"""Admin's forms."""

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.blog.models import Author, BlogPost, Tag


class AuthorForm(forms.ModelForm):
    """Author form for adding, updating author."""

    class Meta:
        """Meta configs for model."""

        model = Author
        widgets = {
            'name': forms.TextInput(),
            'appointment': forms.TextInput(),
        }
        fields = '__all__'


class BlogPostForm(forms.ModelForm):
    """Form for adding, updating blog post."""

    class Meta:
        """Meta configs for model."""

        model = BlogPost
        widgets = {
            'title': forms.TextInput(),
            'short_description': CKEditorUploadingWidget(),
            'text': CKEditorUploadingWidget(),
        }
        fields = '__all__'


class TagForm(forms.ModelForm):
    """Form for adding, updating blog tag."""

    class Meta:
        """Meta configs for model."""

        model = Tag
        widgets = {
            'title': forms.TextInput()
        }
        fields = '__all__'
