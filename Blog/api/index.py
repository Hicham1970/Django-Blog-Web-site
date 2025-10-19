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
def handler(request, response):
    # Handle the request using Django's WSGI application
    return application(request.environ, response.start_response)
