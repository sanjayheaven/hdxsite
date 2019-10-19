from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from blog.models import Post

from simditor.fields import RichTextField


class BaseComment(models.Model):
    '''
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    # content = models.TextField(verbose_name='正文',max_length=1024)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        abstract = True###不会对应数据库


class Comment(BaseComment):
    '''
    '''
    content = RichTextField(verbose_name='评论正文')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',verbose_name='文章')#related_name反向查询

    def __str__(self):
        return 'comment'

    class Meta:
        verbose_name = verbose_name_plural = '评论'
        ordering = ['-created_time']


class CommentReply(BaseComment):
    '''
    '''
    reply_content = RichTextField(verbose_name='正文')
    reply_comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies',blank=True,verbose_name='评论回复')
    reply = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE, verbose_name='回复对象')

    def __str__(self):
        return 'reply'

    class Meta:
        verbose_name = verbose_name_plural = '评论回复'
        ordering = ['-created_time']
