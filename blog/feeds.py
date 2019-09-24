from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class AllPostRssFeed(Feed):
    # 显示在聚会阅读器上的标题
    title = " hdx's blog "
    # 跳转网址，为主页
    link = "/"
    # 描述内容
    description = " hdx's blog update"
    # 需要显示的内容条目，这个可以自己挑选一些热门或者最新的博客

    def items(self):
        return Post.objects.all()[:100]

    # 显示的内容的标题,这个才是最主要的东西
    def item_title(self, item):
        return "【{}】{}".format(item.category,item.title)

    # 显示的内容的描述
    def item_description(self, item):
        return item.abstract

    def item_link(self,item):
        return reverse('blog:post-detail',kwargs={'post_id':item.id})