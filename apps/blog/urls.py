"""Blog app of Smyt blog site URL Configuration."""

from django.urls import path

import apps.blog.views as v

app_name = 'blog'

urlpatterns = [
    path('author/<int:author_id>/<slug:author_slug>/', v.BlogListView.as_view(), name="author"),
    path('author/<int:author_id>/', v.BlogListView.as_view(), name="author"),
    path('tag/<slug:tag_slug>/', v.BlogListView.as_view(), name="tag"),
    path('<slug:slug>/', v.BlogPostView.as_view(), name="post"),
    path('', v.BlogListView.as_view(), name='index'),
]
