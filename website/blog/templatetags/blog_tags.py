from django import template
from blog.models import Category

register = template.Library()   # через него происходит регистрация тегов

all_categories = {'title': 'Все категории', 'slug': 'all-categories'}


@register.inclusion_tag('blog/categories_tag.html')
def show_categories(cat_selected=0):
    categories = Category.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected, 'all_categories': all_categories}
