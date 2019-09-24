from .base import * # NOQA


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hdxsite',
        'USER': 'root',
        'PASSWORD': os.environ.get('DJANGO_MYSQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 3306,
        
    }
}


