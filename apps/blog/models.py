"""Blog application models."""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.utils.text import gettext_lazy as _


class Author(models.Model):
    """Blog post Author."""

    user = models.OneToOneField(
        User,
        verbose_name=_('Linked user'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.TextField(_('Name'))
    slug = models.SlugField(_('Url name'), default="")
    appointment = models.TextField(_('Position at work'))
    avatar = models.ImageField(_('Avatar'), upload_to="author")

    def avatar_tag(self):
        """Change output avatar field."""
        return mark_safe('<img src="{}" style="max-width: 108px;" />'.format(self.avatar.url))

    avatar_tag.short_description = _('Image')

    def __str__(self):
        """View for Author object."""
        return "{name}, {appointment}".format(
            name=self.name,
            appointment=self.appointment
        )

    class Meta:
        """Meta Class for Author class."""

        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['name']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Author if user created."""
    if created:
        Author.objects.create(
            user=instance,
            name=instance.username
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Author linked with user."""
    instance.author.save()


class Tag(models.Model):
    """Blog tag."""

    title = models.TextField(_('Name'))
    slug = models.SlugField(_('Url name'), unique=True)

    def __str__(self):
        """View for Tag object."""
        return self.title

    class Meta:
        """Meta Class for Tag class."""

        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['title']


class BlogPost(models.Model):
    """Blog post model."""

    title = models.TextField(_('Title'))
    url = models.SlugField(_('Url'), unique=True)
    short_description = models.TextField(_('Short description'))
    text = models.TextField(_('Text'))
    image = models.ImageField(_('Image'), upload_to="articles", null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="blog_posts", blank=True)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    views_count = models.IntegerField(_('Views count'), default=0)
    real_views_count = models.IntegerField(_('Real views count'), default=0)
    published_at = models.DateTimeField(_('Date published'), null=True, blank=True)
    is_published = models.BooleanField(_('Is publish?'))

    def __str__(self):
        """View for BlogPost object."""
        return "{title}, id: {pk}".format(
            title=self.title,
            pk=self.pk,
        )

    class Meta:
        """Meta Class for BlogPost class."""

        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
