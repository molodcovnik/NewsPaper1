from rest_framework import serializers
from news.models import Post, Author, PostCategory, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        #fields = ('name_category',)
        fields = ('id', 'name_category',)

class PostCategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='category.id')
    category = CategorySerializer()


    class Meta:
        model = PostCategory
        #fields = ('category',)
        fields = ('id', 'category')


class PostSerializer(serializers.ModelSerializer):
    time_add = serializers.ReadOnlyField()
    author_id = serializers.ReadOnlyField(source='author.id')
    author = serializers.ReadOnlyField(source='author.authorUser.username')
    category_post = PostCategorySerializer(source='postcategory_set', many=True)

    class Meta:
        model = Post
        depth = 1
        fields = ['id',
                  'author',
                  'author_id',
                  'category_type',
                  'header_post',
                  'text',
                  'category_post',
                  'time_add']




class PostCreateSerializer(serializers.ModelSerializer):
    category_post = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = ['author',
                  'category_type',
                  'header_post',
                  'text',
                  'category_post',
                  'time_add',]

