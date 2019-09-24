from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.

from .models import Comment,CommentReply


class CommentAdmin(admin.ModelAdmin):
    '''
    显示
    '''
    list_display = ('id','post','content', 'owner','created_time')
    ordering = ['id']
    list_filter = ['post','owner']
    # actions_on_bottom = False #默认为是false，
    # actions_on_top = True #默认为True，
    # search_fields = ['name']###
    '''
    编辑
    '''
    # save_on_top = True##增加时候用到，保存按钮在上方
    # fieldsets = [
    #     ('Name', {
    #         'fields': ['name']
    #     }),
    #     ('owner', {
    #         'fields': ['owner'],
    #     }),
    # ]

    # inlines = [PostInline,]

admin.site.register(Comment,CommentAdmin)


class CommentReplyAdmin(admin.ModelAdmin):
    # list_display = ('id','name', 'owner', 'created_time')
    list_display = ('id','reply_comment','reply_content','reply','owner', 'created_time')
    ordering = ['id']
    # save_on_top = True


admin.site.register(CommentReply, CommentReplyAdmin)
