from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating_post'))
        pRat = 0
        pRat += postRat.get('postRating')# if postRat.get('postRating') else 0

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating_comment'))
        cRat = 0
        cRat += commentRat.get('commentRating')# if commentRat.get('commentRating') else 0

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    news = 'NEWS'
    article = 'ART'

    TYPE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=4,
                                choices=TYPE,
                                default=news)

    time_add = models.DateTimeField(auto_now_add=True)
    category_post = models.ManyToManyField(Category, through='PostCategory')
    header_post = models.CharField(max_length=128)
    text = models.TextField()
    rating_post = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.header_post},{self.text},{self.time_add}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.SmallIntegerField(default=0)

    def __str__(self):
        return {self.text_comment}, {self.comment_user}, {self.time_comment}

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('comment_create', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


