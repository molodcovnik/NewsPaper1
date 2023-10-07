from django.contrib.auth.models import User
from django.db.models import Count, F, Subquery
from rest_framework import generics, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer, CategorySerializer, PostCreateSerializer, StaticSerializer
# AuthorSerializer, UserSerializer, CategorySerializer
from news.models import Post, Author, PostCategory, Category


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-time_add')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class PostCreateViewSet(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save()
        # try:
        #     serializer.save(author=self.request.user)
        # except:
        #     raise ValidationError('Нет доступа')

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        category = Category.objects.get(name_category=request.data['name_category'])
        if serializer.is_valid():
            serializer.add(category)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def create(self, request):
#     serializer = self.get_serializer(data=request.data)
#     category = Category.objects.get(pk=request.data['category'])
#     if serializer.is_valid():
#         serializer.save(category=category)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribersStaticView(APIView):

    def get(self, request, format=None):
        category_list = Category.objects.all().values_list('pk', flat=True)
        res = Category.objects.values('id', 'name_category') \
            .annotate(count=Count('subscribers__username')) \
            .order_by('-count')

        serializer = StaticSerializer(res, many=True, )
        return Response(serializer.data)
