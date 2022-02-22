from .base import *

# 本地环境

ALLOWED_HOSTS = ['127.0.0.1']

LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "admin"

LDAP_AUTH_URL = "ldap://114.117.165.121:389"

SECRET_KEY = 'django-insecure-+t-lk5m0*2vqsvt9^5!r_q@(8#zih^ge^wskfrg9w)$6bnp#m6'

# 钉钉webhook地址
DINGTALK_WEB_HOOK = 'https://oapi.dingtalk.com/robot/send?access_token=b73fb497e1eacb551474caa7041bb8b975198331ceba87667d5b151a76d6e745'

DEBUG = True

INSTALLED_APPS += (
    # debug toolbar
)
