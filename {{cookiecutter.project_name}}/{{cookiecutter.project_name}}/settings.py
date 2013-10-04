from os.path import abspath, dirname, join
from configurations import Configuration, values

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
PROJECT_NAME = '{{cookiecutter.project_name}}'


class RedisCache(object):
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '127.0.0.1:6379',
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            },
        },
    }


class Common(Configuration):
    ADMINS = (
        # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '{{ secret_key }}'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []


    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'discover_runner',
        'django_jenkins',
        'raven.contrib.django.raven_compat',
        'debug_toolbar',
        'floppyforms',
    ]

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    ROOT_URLCONF = '{{cookiecutter.project_name}}.urls'

    WSGI_APPLICATION = '{{cookiecutter.project_name}}.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.sqlite',
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

    LANGUAGE_CODE = 'en-GB'

    TIME_ZONE = 'Europe/London'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = join(PROJECT_ROOT, 'static_root')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = join(PROJECT_ROOT, 'media')

    # Additional locations of static files
    STATICFILES_DIRS = [
        join(PROJECT_ROOT, 'static')
    ]

    TEMPLATE_DIRS = [
        join(PROJECT_ROOT, 'templates')
    ]

    TEST_RUNNER = 'discover_runner.DiscoverRunner'

    FIXTURE_DIRS = [
        join(PROJECT_ROOT, 'fixtures')
    ]

    # App settings

    # django-jenkins
    PROJECT_APPS = [app for app in INSTALLED_APPS if app.startswith('{{cookiecutter.project_name}}.')]
    JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                     'django_jenkins.tasks.django_tests',
                     'django_jenkins.tasks.run_pep8',
                     'django_jenkins.tasks.with_coverage')

    # django-debug-toolbar
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    INTERNAL_IPS = ('127.0.0.1',)


class Dev(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/app-emails'


class Deployed(RedisCache, Common):
    """
    Settings which are for a non local deployment, served behind nginx.
    """
    PUBLIC_ROOT = join(PROJECT_ROOT, '../public/')
    STATIC_ROOT = join(PUBLIC_ROOT, 'static')
    MEDIA_ROOT = join(PUBLIC_ROOT, 'media')
    COMPRESS_OUTPUT_DIR = ''

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''
    SERVER_EMAIL = ''


class Stage(Deployed):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'OPTIONS': {
                'autocommit': True,  # see https://docs.djangoproject.com/en/dev/ref/databases/#autocommit-mode
            }
        }
    }


class Prod(Deployed):
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'OPTIONS': {
                'autocommit': True,  # see https://docs.djangoproject.com/en/dev/ref/databases/#autocommit-mode
            }
        }
    }

    ALLOWED_HOSTS = ['', ]  # add deployment domain here

    RAVEN_CONFIG = {
        'dsn': ''  # add sentry DSN
    }