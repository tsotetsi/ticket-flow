from .base import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = os.getenv('DEBUG', 1)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.getenv('SECRET_KEY', 'changeMeIfYouSeeThis')

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# TODO: Set static IP address for minikube, minikube start --static=192.168.49.2
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104