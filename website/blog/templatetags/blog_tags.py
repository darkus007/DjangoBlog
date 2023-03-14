from django import template
from django.core.cache import cache

from blog.models import Category
from members.models import Profile

from website.settings import ALL_CATEGORIES

register = template.Library()


@register.inclusion_tag('blog/categories_tag.html')
def show_categories(cat_selected=None):
    categories = cache.get_or_set('categories', Category.objects.values('title', 'slug'), 300)
    return {'categories': categories, 'cat_selected': cat_selected, 'all_categories': ALL_CATEGORIES}


@register.simple_tag()
def get_user_profile(user):
    return cache.get_or_set(f'{user.username}_profile', Profile.objects.filter(user=user.pk).values('slug'), 300)
