"""
Django settings for portfolio_project project.

Generated by 'django-admin startproject' using Django 4.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure--(fgtx4!ac=p)41t0jhfkahcve!fd2@f2po2odx#a$9hdda1z#')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'storages',
    
    # Local apps
    'portfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'

TEMPLATES = [
    {
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
    },
]

WSGI_APPLICATION = 'portfolio_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# データベース設定
DATABASE_URL = os.getenv('SUPABASE_DATABASE_URL')

if DATABASE_URL:
    # Supabase PostgreSQL設定
    import dj_database_url
    db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    
    # IPv6問題を回避するための設定
    db_config['OPTIONS'] = {
        'sslmode': 'require',
        'options': '-c default_transaction_isolation=serializable'
    }
    
    DATABASES = {
        'default': db_config
    }
else:
    # SQLiteフォールバック
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise設定
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# メディアファイル設定
USE_SUPABASE_STORAGE = os.getenv('SUPABASE_STORAGE_ACCESS_KEY_ID') is not None

if USE_SUPABASE_STORAGE:
    # Supabase Storage設定
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.getenv('SUPABASE_STORAGE_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('SUPABASE_STORAGE_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('SUPABASE_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('SUPABASE_STORAGE_REGION')
    AWS_S3_ENDPOINT_URL = os.getenv('SUPABASE_STORAGE_ENDPOINT')
    AWS_S3_CUSTOM_DOMAIN = f'tvocxlxchmzdwtmkvirh.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = True
    AWS_S3_VERIFY = True
    
    MEDIA_URL = f'https://tvocxlxchmzdwtmkvirh.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}/'
else:
    # ローカルストレージ設定
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Django Allauth 設定
SITE_ID = 1

# 認証バックエンド
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth 設定
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_LOGOUT_ON_GET = True

# Login URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/portfolio/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
