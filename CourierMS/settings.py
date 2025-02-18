from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r$u!z*53x(l@c8(5@&pu*v6dsd_%@+e4r=@+j7ag#l5p0g*#+0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',  # Make sure your app is listed here
    'bootstrap4',  # If you're using Bootstrap for UI
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CourierMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Consider specifying templates directory for your app here
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

WSGI_APPLICATION = 'CourierMS.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Login settings
LOGIN_REDIRECT_URL = 'courier_dashboard'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Media files (For handling file uploads like images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Google Maps API Key
GOOGLE_MAPS_API_KEY = 'AIzaSyC95lObpySHqUA0UvzP8ETE_gOW8EKSnfU'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Email configuration (place this towards the end)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use 587 for TLS, 465 for SSL
EMAIL_USE_TLS = True  # Set to True for TLS
EMAIL_USE_SSL = False  # Make sure SSL is False
EMAIL_HOST_USER = 'laurencemmarete@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'Muriithi39_'  # Your Gmail app password
DEFAULT_FROM_EMAIL = 'laurencemmarete@gmail.com'  # The sender email address
