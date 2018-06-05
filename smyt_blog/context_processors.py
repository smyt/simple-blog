"""Smyt blog site context processors."""

from django.conf import settings


def django_settings(request):
    """Adding django settings to context."""
    return {
        'settings': {
            'BASE_NAME': settings.BASE_NAME
        }
    }
