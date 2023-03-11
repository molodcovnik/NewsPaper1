from django import forms
from .models import Post, Comment

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


class CommentForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['comment_post'].disabled = True
    #     self.fields['comment_user'].disabled = True
    class Meta:
        model = Comment
        fields = [
            'comment_post',
            'comment_user',
            'text_comment',
        ]


