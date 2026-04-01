from .settings import *

import cloudinary

# Cloudinary configuration for production media storage
cloudinary.config(
    cloud_name="doh12ravy",
    api_key="799647489875273",
    api_secret="mukXbTW"
)

# Use Cloudinary for file storage in production
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DEBUG = False

# Disable DB writes for readonly
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        },
        'DISABLE_SERVER_SIDE_CURSOR': True,
    }
}

# Simplified apps - removed ckeditor/dashboard
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Home',
]

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {'django': {'handlers': ['console'], 'level': 'ERROR'}},
}

