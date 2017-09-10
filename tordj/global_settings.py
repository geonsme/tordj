# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""default settings. all attribute here can be overridden"""

DATABASES = {
    'session': {
        'ENGINE': 'redis',
        'OPTIONS':{
            'host': 'localhost',
            'port': 6379,
            'db': 0,
        }
    },
}  # database config


TEMPLATES = [
    {
        'BACKEND': 'tordj.template.jinja2_backend.Jinja2Engine',
        'APP_DIRS': True,
        'DIRS': [],
        'OPTIONS': {
            'extensions': ['jinja2.ext.loopcontrols'],
        },
    },
]

MIDDLEWARE = []     # middlewares

INSTALLED_APPS = []     # apps

DEBUG = False       # debug switch

TEMPLATES = []      # template config

SECRET_KEY = ''

SESSION_SERIALIZER = 'json' # json/pickle/cPickle and etc. make sure this module has `loads` and `dumps` method

SESSION_COOKIE_NAME = 'sessionid'

SESSION_COOKIE_HMAC_NAME = 'verification'

ROUTER_MODULE = "urls.urlpatterns"

STATIC_URL = '/static/'

STATIC_FOLDERNAME = 'static'

STATIC_PATH = None  

GRPC_SERVICES = {}  # with format like this {'service module': {'env': 'environment module'}, } 
                    # eg.  {
                    #           "tordj.grpcio.dbservice": {
                    #               "context": "path to context dict",  # if has not special context, just let empty
                    #           }, 
                    #       } 



GRPC_SERVER_CONFIG = {
    'ip': '[::]',
    'port': 50051,
    'workers': 10,
}

GRPC_CLIENT_CONFIG = {
    'host': 'localhost',
    'port': 50051,
}

TONADO_CONFIG = {}