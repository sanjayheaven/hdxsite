"""hdxsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap

from blog.feeds import AllPostRssFeed
from blog.sitemaps import PostSitemap
from django.contrib.auth import views as auth_views

import notifications.urls

sitemaps = {
    'posts':PostSitemap,
}


urlpatterns = [
    # path('',),####    参考链接默认值？？？
    path('', include('blog.urls'),name='blog'),
    path('comment/', include('comment.urls'),name='comment'),
    path('tool/', include('tool.urls'),name='tool'),
    path('accounts/', include('allauth.urls'),name='allauth'),

    path('simditor/', include('simditor.urls'),name='simditor'),
    path('inbox/notifications/', include('notifications.urls'),name='notifications'),

    path('rss/feed/', AllPostRssFeed(),name='RSS'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('admin/',admin.site.urls),

    
]
