from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['a0c208cd3ea0.ngrok.io',
'127.0.0.1']