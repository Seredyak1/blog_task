from django.contrib import admin

from .models import Blog, Post


class BlogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'updated_at')
    list_filter = ('user', 'updated_at')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'updated_at')
    list_filter = ('user', 'updated_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Blog, BlogAdmin)
