from django.contrib import admin
from django.contrib.admin import options
from .models import (
    Post,
    Tag,
    Media,
    PostLike
)


class PostImageInline(options.TabularInline):
    """
    Inline for media
    """
    model = Media
    extra = 1  # number of image line


class PostAdmin(admin.ModelAdmin):
    """
    Admin class for model post
    """
    inlines = [PostImageInline]
    list_display = ('description', 'get_tags', 'likes', 'dislikes')


class TagAdmin(admin.ModelAdmin):
    """
    Admin class for model tag
    """
    list_display = ('name', 'weight')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PostLike)
