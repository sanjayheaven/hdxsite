from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.

from .models import Category,Post,Tag

# admin.site.register(Category)
# admin.site.register(Tag)
# admin.site.register(Post)

class PostInline(admin.StackedInline):
    model = Post
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    '''
    显示
    '''
    list_display = ('id','name', 'owner','created_time')
    ordering = ['id']
    list_filter = ['name']
    # actions_on_bottom = False #默认为是false，
    # actions_on_top = True #默认为True，
    search_fields = ['name']###
    
    '''
    编辑
    '''
    # save_on_top = True##增加时候用到，保存按钮在上方
    fieldsets = [
        ('Name', {
            'fields': ['name']
        }),
        ('owner', {
            'fields': ['owner'],
        }),
    ]

    inlines = [PostInline,]

admin.site.register(Category,CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    '''
    显示
    '''
    list_display = ('id','title','abstract', 'content','category','status','total_views','owner','created_time',)
    ordering = ['id']
    list_filter = ['title']
    # actions_on_bottom = False #默认为是false，
    # actions_on_top = True #默认为True，
    search_fields = ['title']###
    
    '''
    编辑
    '''
    # save_on_top = True##增加时候用到，保存按钮在上方
    fields = (
        ('category','title'),
        ('owner','status'),
        'abstract',
        'content',
        'tag',
    )
    # filter_vertical = ('tag', )
    filter_horizontal = ('tag', )

admin.site.register(Post,PostAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'created_time')
    ordering = ['id']
    # save_on_top = True

admin.site.register(Tag,TagAdmin)






