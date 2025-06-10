from windforlife.settings.base import *  # noqa: F401, F403
import socket

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)  # noqa: F405

if DEBUG:
    # Detect internal IPs for Docker
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = ["127.0.0.1", "localhost"] + [ip[:-1] + "1" for ip in ips]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405


WSGI_APPLICATION = "windforlife.wsgi.dev.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
