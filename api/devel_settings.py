# pull in the normal settings
from settings import *

print "NOTICE: using local devel settings!"

# always debug in devel mode
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NAME_API',
        'USER': 'USER_API',
        'PASSWORD': 'PWD',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

