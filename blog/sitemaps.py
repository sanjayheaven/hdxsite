# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly' #'always''hourly''daily''weekly''monthly''yearly''never' 
    priority = 1.0

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.update_time

    def location(self,obj):
        return reverse('blog:post-detail',kwargs={'post_id':obj.id})