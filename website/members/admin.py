from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'image', 'ya_url', 'vk_url', 'ok_url', 'git_url', 'website_url')
    list_display_links = ('user', 'slug')
    search_fields = ('user', )
    prepopulated_fields = {'slug': ('user',)}


admin.site.register(Profile, ProfileAdmin)
