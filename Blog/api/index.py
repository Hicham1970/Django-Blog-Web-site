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
    Handler for Vercel serverless functions
    """
    from django.core.handlers.wsgi import WSGIHandler
    from io import BytesIO
    import json

    # Create a WSGI environ from the Vercel event
    environ = {
        'REQUEST_METHOD': event.get('method', 'GET'),
        'SCRIPT_NAME': '',
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('query', {}).get('string', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': str(len(event.get('body', ''))),
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(event.get('body', '').encode('utf-8')),
        'wsgi.errors': BytesIO(),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    # Add headers to environ
    for header, value in event.get('headers', {}).items():
        environ[f'HTTP_{header.upper().replace("-", "_")}'] = value

    # Response collector
    status = []
    headers = []
    body = []

    def start_response(status_line, response_headers, exc_info=None):
        status.append(status_line)
        headers.extend(response_headers)

    # Call the WSGI application
    app_response = application(environ, start_response)

    # Collect the response body
    for data in app_response:
        body.append(data)

    # Return Vercel-compatible response
    return {
        'statusCode': int(status[0].split()[0]),
        'headers': dict(headers),
        'body': b''.join(body).decode('utf-8', errors='ignore')
    }
