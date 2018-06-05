"""Configurations admin pages for blog application."""

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import gettext_lazy as _

from apps.blog.admin_forms import AuthorForm, BlogPostForm, TagForm
from apps.blog.models import BlogPost, Author, Tag


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Settings for displaying blog posts."""

    form = BlogPostForm

    list_filter = ('tags', 'author')
    list_display = (
        'title',
        'small_image_tag',
        'get_url_tag',
        'id',
        'real_views_count',
        'is_published',
        'published_at'
    )
    readonly_fields = ('image_tag', 'real_views_count')
    prepopulated_fields = {"url": ("title",)}
    fieldsets = (
        (None, {
            'fields': (
                ('title', 'url', 'is_published'),
                'author',
                'short_description',
                ('image', 'image_tag'),
                'text',
                ('published_at', 'views_count', 'real_views_count'),
                'tags',
            )
        }),
    )

    def get_url_tag(self, obj):
        """Add additional column(link to real post) to list of blog posts."""
        return mark_safe('<a href="{actual_url}">{slug}</a>'.format(
            actual_url=reverse("blog:post", kwargs={"slug": obj.url}),
            slug=obj.url
        ))
    get_url_tag.short_description = _('Link')

    def image_tag(self, obj):
        """Add additional column(image preview) to list of blog posts."""
        return mark_safe('<img src="{}" style="max-height: 108px;" />'.format(obj.image.url)) if obj.image else None
    image_tag.short_description = _('Image')

    def small_image_tag(self, obj):
        """Add additional column(small image preview) to list of blog posts."""
        return mark_safe('<img src="{}" style="max-height: 40px;" />'.format(obj.image.url)) if obj.image else None
    small_image_tag.short_description = ''


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Settings for displaying blog authors."""

    form = AuthorForm

    list_display = ('name', 'appointment', 'id')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('avatar_tag',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Settings for displaying blog tags."""

    form = TagForm

    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug')
