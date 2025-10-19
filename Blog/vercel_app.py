import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')

# Setup Django
django.setup()

# Import the Vercel Django handler
from vercel_django import handler

# Export the handler
app = handler
