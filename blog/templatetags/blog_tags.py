from django import template
from ..models import Category,Post,Tag

register = template.Library()

@register.simple_tag()
def get_category_all():
    return Category.objects.all()

@register.simple_tag()
def get_post_all():
    return Post.objects.all()

@register.simple_tag()
def get_tags_all():
    return Tag.objects.all()


