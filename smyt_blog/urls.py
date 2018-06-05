"""Smyt blog site URL Configuration."""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

import apps.blog.urls

urlpatterns = [
    path('{}admin/'.format(settings.BASE_NAME), admin.site.urls),
    re_path(r'^{}ckeditor/'.format(settings.BASE_NAME), include('ckeditor_uploader.urls')),
    path('{}'.format(settings.BASE_NAME), include(apps.blog.urls, namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
