from django.contrib import admin

from blog.models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )  # столбцы, которые отображаются в админ панели
    list_display_links = ('title', )  # переход на правку записей по этим полям
    search_fields = ('title', )  # последовательность имен полей, по которым должна выполняться фильтрация
    prepopulated_fields = {'slug': ('title',)}  # заполнение поля 'slug' на основании поля 'title'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'cat')  # столбцы, которые отображаются в админ панели
    list_display_links = ('title', )  # переход на правку записей по этим полям
    search_fields = ('title', 'content', 'user', 'cat', 'time_created')  # последовательность имен полей, по которым должна выполняться фильтрация
    prepopulated_fields = {'slug': ('title',)}  # заполнение поля 'slug' на основании поля 'title'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
