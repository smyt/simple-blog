"""Blog app views for smyt blog site."""

from datetime import datetime
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from apps.blog.models import BlogPost


class BlogListView(TemplateView):
    """View with published blog posts."""

    template_name = "index.html"
    DATE_FORMAT = '%Y.%d.%m %H:%M:%S'

    def get_context_data(self, **kwargs):
        """Add additional data to context page."""
        data = super().get_context_data(**kwargs)
        posts = BlogPost.objects.all()\
            .select_related("author")\
            .prefetch_related("tags")\
            .filter(is_published=True)\
            .order_by('-published_at', 'id')

        if 'lastPublished' in self.request.GET:
            last_published = datetime.strptime(self.request.GET['lastPublished'], self.DATE_FORMAT)
            posts = posts.filter(published_at__lt=last_published)

        if 'tag_slug' in kwargs:
            posts = posts.filter(tags__slug__in=(kwargs['tag_slug'], ))

        if 'author_id' in kwargs:
            posts = posts.filter(author=kwargs['author_id'])

        data['has_more'] = posts.count() > 10

        posts = list(posts[:10])
        data['last_published'] = min([i.published_at for i in posts]) if posts else None
        data['last_published'] = data['last_published'].strftime(self.DATE_FORMAT) if data['last_published'] else None
        data['posts'] = posts

        return data

    def get(self, request, *args, **kwargs):
        """Process get request, added additional processing for ajax requests."""
        if self.request.is_ajax():
            data = self.get_context_data(**kwargs)
            return JsonResponse({
                'has_more': data['has_more'],
                'lastPublished': data['last_published'],
                'content': render_to_string("partials/posts_list.html", data, request=self.request)
            })

        return super().get(request, *args, **kwargs)


class BlogPostView(TemplateView):
    """View for displaying a blog post."""

    template_name = "post.html"

    def get_context_data(self, **kwargs):
        """Add additional data to context page."""
        data = super().get_context_data(**kwargs)
        post = get_object_or_404(BlogPost, url=kwargs['slug'])

        if not self.request.user.is_authenticated:
            BlogPost.objects.filter(pk=post.pk).update(
                views_count=F('views_count') + 1,
                real_views_count=F('real_views_count') + 1
            )

        data['post'] = post
        return data
