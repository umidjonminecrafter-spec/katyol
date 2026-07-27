import os
from pathlib import Path
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'kotyol-erp-super-secret-jwt-key-2026-production-ready')

DEBUG = os.getenv('ENVIRONMENT', 'development') == 'development'

ALLOWED_HOSTS = ['*']

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Kotyol ERP Backend')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
API_V1_STR = '/api/v1'

# JWT Settings
JWT_SECRET_KEY = SECRET_KEY
JWT_ALGORITHM = 'HS256'
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '7'))

# Superadmin
SUPERADMIN_USERNAME = os.getenv('SUPERADMIN_USERNAME', '+998901234567')
SUPERADMIN_PASSWORD = os.getenv('SUPERADMIN_PASSWORD', 'Password123!')

# File Upload
UPLOAD_DIR = os.getenv('UPLOAD_DIR', os.path.join(BASE_DIR, 'uploads'))
MAX_FILE_SIZE_MB = 15
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.pdf', '.xlsx', '.docx']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'corsheaders',
    'apps.accounts',
    'apps.audit',
    'apps.dashboard',
    'apps.files',
    'apps.finance',
    'apps.master_data',
    'apps.production',
    'apps.products',
    'apps.purchasing',
    'apps.sales',
    'apps.warehouse',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('DATABASE_PATH', os.path.join(BASE_DIR, 'kotyol.db')),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'x-branch-id',
    'X-Branch-ID',
    'authorization',
]
APPEND_SLASH = False


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'UNAUTHENTICATED_USER': None,
}

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

MEDIA_URL = '/uploads/'
MEDIA_ROOT = UPLOAD_DIR

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Logging
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
