from django import template
from ..models import Comment

from blog.models import Post,Tag,Category


register = template.Library()

@register.simple_tag()
def get_comments_all(post_id):
    return Category.objects.all().filter(post__id=post_id)


