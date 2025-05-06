from windforlife.settings.base import *

DEBUG = False

allowed_hosts_env = os.getenv("ALLOWED_HOSTS")
ALLOWED_HOSTS = [host for host in allowed_hosts_env.split(",") if host] if allowed_hosts_env else []

WSGI_APPLICATION = "windforlife.wsgi.prod.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
