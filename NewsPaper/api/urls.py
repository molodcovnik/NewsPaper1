from django.urls import path
from .views import PostList, CategoryList, PostCreateViewSet, SubscribersStaticView


urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/create/', PostCreateViewSet.as_view()),
    path('category/', CategoryList.as_view()),
    path('subs/', SubscribersStaticView.as_view()),
]