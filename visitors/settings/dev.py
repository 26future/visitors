from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['4f1aae4c4b06.ngrok.io',
'127.0.0.1']