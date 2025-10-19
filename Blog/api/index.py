import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

# Import Django and setup
import django
django.setup()

# Run collectstatic on first import
from django.core.management import execute_from_command_line
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
except:
    pass  # Ignore if already collected

# Import the WSGI application
from Blog.wsgi import application

# Vercel expects a function called 'handler'
def handler(request, response):
    # Handle the request using Django's WSGI application
    return application(request.environ, response.start_response)
