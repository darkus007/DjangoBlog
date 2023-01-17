from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    # столбцы, которые отображаются в админ панели
    list_display = ('user', 'slug', 'image', 'ya_url', 'vk_url', 'ok_url', 'git_url', 'website_url')
    list_display_links = ('user', 'slug')  # переход на правку записей по этим полям
    search_fields = ('user', )  # последовательность имен полей, по которым должна выполняться фильтрация
    prepopulated_fields = {'slug': ('user',)}  # заполнение поля 'slug' автоматически на основании поля 'title'


admin.site.register(Profile, ProfileAdmin)
