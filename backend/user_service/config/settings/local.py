from .base import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = os.getenv('DEBUG', 1)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.getenv('SECRET_KEY', 'changeMeIfYouSeeThis')

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# TODO: Set static IP address for minikube, minikube start --static=192.168.49.2
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "user-service"]  # noqa: S104

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = os.getenv("EMAIL_HOST", default="mailpit")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 1025         # Mailpit's SMTP port
EMAIL_USE_TLS = False     # Mailpit does not use TLS by default
EMAIL_USE_SSL = False     # Mailpit does not use SSL by default

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # Disable profiling panel due to an issue with Python 3.12:
        # https://github.com/jazzband/django-debug-toolbar/issues/1875
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"