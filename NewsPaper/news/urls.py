from django.urls import path
from .views import (
     PostList, PostDetail, PostSearch, PostCreate, PostEdit, PostDelete, get_author_status, CategoryListView, subscribe, unsubscribe,
)
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path('', index, name='post_list'),
    path('', cache_page(5)(PostList.as_view()), name='post_list'),
    path('<int:pk>', cache_page(5)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('author/', get_author_status, name='author_status'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    #path('<int:pk>/comment/', CommentCreate.as_view(), name='comment_create'),
]
