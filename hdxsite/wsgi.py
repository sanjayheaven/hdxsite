"""
WSGI config for hdxsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hdxsite.settings')
profile = os.environ.get('HDX_DISITE_PROFILE','product')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hdxsite.setting.{}'.format(profile))

application = get_wsgi_application()
