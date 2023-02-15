from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'category_type',
            'category_post',
            'header_post',
            'text',
        ]