from django.core.wsgi import get_wsgi_application
from django.conf import settings
import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

# Setup Django
import django
django.setup()

# Vercel expects a function called 'handler'
def handler(event, context):
    """
    Vercel serverless handler for Django
    """
    try:
        from django.core.handlers.wsgi import WSGIHandler
        from io import BytesIO
        import json
        import base64

        # Create WSGI environ from Vercel event
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
        response_headers = []

        def start_response(status_line, headers_list, exc_info=None):
            status.append(status_line)
            response_headers.extend(headers_list)

        # Create WSGI handler and process request
        wsgi_handler = WSGIHandler()
        response_iter = wsgi_handler(environ, start_response)

        # Collect response body
        response_body = b''.join(response_iter)

        # Prepare response
        response = {
            'statusCode': int(status[0].split()[0]) if status else 200,
            'headers': dict(response_headers),
        }

        # Determine content type for encoding
        content_type = ''
        for header_name, header_value in response_headers:
            if header_name.lower() == 'content-type':
                content_type = header_value.lower()
                break

        # Handle binary vs text response
        if any(ct in content_type for ct in ['image', 'application', 'font', 'audio', 'video']):
            response['body'] = base64.b64encode(response_body).decode('utf-8')
            response['isBase64Encoded'] = True
        else:
            response['body'] = response_body.decode('utf-8', errors='replace')

        return response

    except Exception as e:
        print(f"Handler error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e), 'type': 'handler_error'})
        }
