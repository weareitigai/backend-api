"""
Django settings for config project.
"""

from pathlib import Path
from decouple import config
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-railway-default-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS configuration for deployment
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Render domains
    '.railway.app',   # Railway domains (keeping for compatibility)
    '*'  # Fallback for other deployments
]

# Application definition
DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',
    'django_filters',
    'import_export',
    'admin_honeypot',
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.partner',
    'apps.common',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Handle Railway deployment where DATABASE_URL might not be available initially
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Railway environment with DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
else:
    # Fallback for local development or when DATABASE_URL is not set
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='travel_partner_db'),
            'USER': config('DB_USER', default='travel_partner_user'),
            'PASSWORD': config('DB_PASSWORD', default='your_password_here'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'authentication.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static files configuration for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings - Optimized for performance
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024  # 2MB - Reduced for faster processing
DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024   # 2MB - Reduced for faster processing
FILE_UPLOAD_TEMP_DIR = BASE_DIR / 'temp'  # Temporary directory for file processing
FILE_UPLOAD_PERMISSIONS = 0o644  # File permissions
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755  # Directory permissions

# Create temp directory if it doesn't exist
import os
if not os.path.exists(FILE_UPLOAD_TEMP_DIR):
    os.makedirs(FILE_UPLOAD_TEMP_DIR, exist_ok=True)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_ALL_ORIGINS = DEBUG

# Spectacular Configuration (API Documentation)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Travel Partner API',
    'DESCRIPTION': '''
    # Travel Partner API Documentation
    
    This API provides comprehensive functionality for travel partner management, including:
    
    ## Features
    
    ### Authentication & User Management
    - Email and mobile OTP verification
    - User registration and login
    - Password management and recovery
    - Profile management
    
    ### Partner Onboarding
    - Multi-step partner registration process
    - Business details management
    - Location coverage configuration
    - Tours and services information
    - Legal and banking details
    
    ### Tour Management
    - **AI-powered tour scraping** from travel websites
    - Comprehensive tour data structure with pricing, destinations, and inclusions
    - Tour creation, updating, and management
    - Advanced filtering and search capabilities
    
    ## Key Endpoints
    
    ### Tour Scraping
    - `POST /api/partner/scrape-tour-details/` - Extract tour data from URLs using AI
    
    ### Tour Management
    - `POST /api/partner/user/{user_id}/tours/create/` - Create new tours
    - `GET /api/partner/user/{user_id}/tours/` - List all tours with filtering
    - `GET /api/partner/user/{user_id}/tours/{tour_id}/` - Get tour details
    - `PATCH /api/partner/user/{user_id}/tours/{tour_id}/update/` - Update tours
    
    ## Authentication
    
    Most endpoints require authentication using Token Authentication:
    ```
    Authorization: Token <your_token>
    ```
    
    ## Tour Data Schema
    
    The API supports comprehensive tour data including:
    - Basic tour information (title, destinations, duration)
    - Pricing and availability details
    - Inclusions and exclusions
    - Promotional offers and discounts
    - SEO and marketing information
    
    ## AI-Powered Features
    
    - **Smart Tour Scraping**: Automatically extracts tour details from travel websites
    - **Data Enhancement**: AI models enhance and structure scraped data
    - **Intelligent Categorization**: Automatic categorization and tagging of tours
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SECURITY': [
        {
            'Token': []
        }
    ],
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token-based authentication. Use format: Token <your_token>'
        }
    },
    'TAGS': [
        {
            'name': 'Authentication',
            'description': 'User authentication and authorization endpoints'
        },
        {
            'name': 'Partner Onboarding',
            'description': 'Multi-step partner registration and onboarding process'
        },
        {
            'name': 'Tour Management',
            'description': 'AI-powered tour scraping and comprehensive tour management'
        },
        {
            'name': 'Common Data',
            'description': 'Reference data for destinations, languages, and tour types'
        }
    ]
}

JAZZMIN_SETTINGS = {
    "site_title": "Travel Partner Admin",
    "site_header": "Travel Partner",
    "site_brand": None, # Will default to site_header
    "site_logo": None,  # Remove the logo
    "login_logo": None,  # Optional: path to your login logo
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to the Travel Partner Admin",
    "copyright": "Travel Partner Ltd.",
    "search_model": ["authentication.User", "partner.Partner"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Partner App", "app": "partner"},
        {"model": "authentication.User"},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "authentication.User"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["authentication", "partner", "common"],
    "icons": {
        "auth": "fas fa-users-cog",
        "authentication.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "partner.partner": "fas fa-handshake",
        "partner.businessdetails": "fas fa-briefcase",
        "partner.locationcoverage": "fas fa-map-marked-alt",
        "partner.toursservices": "fas fa-route",
        "partner.legalbanking": "fas fa-balance-scale",
        "common.destination": "fas fa-globe-asia",
        "common.language": "fas fa-language",
        "common.tourtype": "fas fa-hiking",
        "common.timezone": "fas fa-clock",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"authentication.user": "collapsible", "auth.group": "vertical_tabs"},
}

# Email Configuration
# Support for both SendGrid and SMTP backends
EMAIL_BACKEND_TYPE = config('EMAIL_BACKEND', default='console')
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@travelpartner.com')
FROM_NAME = config('FROM_NAME', default='Travel Partner Platform')

if EMAIL_BACKEND_TYPE == 'sendgrid' and SENDGRID_API_KEY:
    # Use SendGrid for email sending
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # We'll override in utils
elif DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Fallback to SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    if not DEFAULT_FROM_EMAIL:
        DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Twilio Configuration (for SMS)
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='')

# Celery Configuration (optional)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# OTP Configuration
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 10

# Feature Flags
MOBILE_OTP_ENABLED = config('MOBILE_OTP_ENABLED', default=False, cast=bool)  # Temporarily disabled

# Rate Limiting Configuration
RATE_LIMIT_OTP_REQUESTS = 3  # Maximum OTP requests per hour
RATE_LIMIT_OTP_WINDOW = 3600  # Time window in seconds (1 hour)

# Cache Configuration for Rate Limiting
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# OpenAI Configuration (optional - for enhanced scraping)
OPENAI_API_KEY = config('OPENAI_API_KEY', default=None)

# Google Gemini Configuration (alternative AI for enhanced scraping)
GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)

# Firecrawl Configuration (for enhanced web scraping)
FIRECRAWL_API_KEY = config('FIRECRAWL_API_KEY', default=None)
