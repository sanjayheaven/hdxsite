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


DEBUG = True ##NOQA PEP8 不需要检测这行，也可以在头增加# flake8: NOQA 这个文件不需要检测

##这里测试最好讲数据库也拿出来改变，使用内置的数据库
