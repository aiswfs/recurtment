from .base import *

# 本地环境

ALLOWED_HOSTS = ['127.0.0.1']

LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "admin"

LDAP_AUTH_URL = "ldap://114.117.165.121:389"

SECRET_KEY = 'django-insecure-+t-lk5m0*2vqsvt9^5!r_q@(8#zih^ge^wskfrg9w)$6bnp#m6'

DEBUG = True

INSTALLED_APPS += (
    # debug toolbar
)
