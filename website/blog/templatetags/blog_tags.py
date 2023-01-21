from django import template
from blog.models import Category

from website.settings import ALL_CATEGORIES

register = template.Library()   # через него происходит регистрация тегов

# all_categories = {'title': 'Все категории', 'slug': 'all-categories'}


@register.inclusion_tag('blog/categories_tag.html')
def show_categories(cat_selected=None):
    categories = Category.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected, 'all_categories': ALL_CATEGORIES}
