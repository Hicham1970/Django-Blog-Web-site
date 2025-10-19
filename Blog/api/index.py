import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

# Import Django and setup
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Configure Django settings for production
if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'fallback-key-change-in-production'),
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'Home',
            'ckeditor',
            'dashboard',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },
        STATIC_URL='/static/',
        STATIC_ROOT=BASE_DIR / 'staticfiles',
        MEDIA_URL='/media/',
        MEDIA_ROOT=BASE_DIR,
        ROOT_URLCONF='Blog.urls',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        USE_TZ=True,
        USE_I18N=True,
        LANGUAGE_CODE='en-us',
        TIME_ZONE='UTC',
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    )

django.setup()

# Get the WSGI application
application = get_wsgi_application()

# Vercel expects a function called 'handler'
def handler(event, context):
    """
    Handler for Vercel serverless functions using Django's built-in WSGI handler
    """
    try:
        from django.core.handlers.wsgi import WSGIHandler
        from io import BytesIO
        import json
        import base64

        # Debug: Print event structure
        print("Event received:", json.dumps(event, indent=2))

        # Create a WSGI environ from the Vercel event
        environ = {
            'REQUEST_METHOD': event.get('method', 'GET'),
            'SCRIPT_NAME': '',
            'PATH_INFO': event.get('path', '/'),
            'QUERY_STRING': '',
            'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
            'CONTENT_LENGTH': '0',
            'SERVER_NAME': 'vercel',
            'SERVER_PORT': '443',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(),
            'wsgi.errors': BytesIO(),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

        # Handle query parameters
        query_params = event.get('query', {})
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            environ['QUERY_STRING'] = query_string

        # Handle request body
        body = event.get('body', '')
        if body:
            if event.get('isBase64Encoded', False):
                body = base64.b64decode(body).decode('utf-8')
            environ['wsgi.input'] = BytesIO(body.encode('utf-8'))
            environ['CONTENT_LENGTH'] = str(len(body))

        # Add headers to environ
        headers = event.get('headers', {})
        for header, value in headers.items():
            key = f'HTTP_{header.upper().replace("-", "_")}'
            environ[key] = value

        # Response collector
        status = []
        headers = []
        body_parts = []

        def start_response(status_line, response_headers, exc_info=None):
            status.append(status_line)
            headers.extend(response_headers)

        # Use Django's WSGIHandler directly
        django_handler = WSGIHandler()
        app_response = django_handler(environ, start_response)

        # Collect the response body
        for data in app_response:
            if isinstance(data, str):
                body_parts.append(data.encode('utf-8'))
            else:
                body_parts.append(data)

        response_body = b''.join(body_parts)

        # Determine if response is binary or text
        content_type = ''
        for header_name, header_value in headers:
            if header_name.lower() == 'content-type':
                content_type = header_value.lower()
                break

        # Prepare response
        response = {
            'statusCode': int(status[0].split()[0]) if status else 200,
            'headers': dict(headers),
        }

        # Handle binary vs text response
        if 'image' in content_type or 'application' in content_type or 'font' in content_type:
            response['body'] = base64.b64encode(response_body).decode('utf-8')
            response['isBase64Encoded'] = True
        else:
            response['body'] = response_body.decode('utf-8', errors='ignore')

        print("Response:", response['statusCode'])
        return response

    except Exception as e:
        print("Error in handler:", str(e))
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
