from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'header_post', 'category_type', 'rating_post')
    list_filter = ('author', 'category_type', 'rating_post')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'text_comment', 'time_comment', 'comment_post')
    list_filter = ('comment_user', 'comment_post')


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory)