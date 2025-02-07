from .base import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "nJF7857vESYkIayySmQySmvPmumtfsttzIRhgy1bOvf3gNaYDeqW2G7Hvv7qAxxa"

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# TODO: Set static IP address for minikube, minikube start --static=192.168.49.2
# ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104
ALLOWED_HOSTS = ["*"]
