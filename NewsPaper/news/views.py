import logging
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Author, Category, PostCategory, Comment
from .filters import PostFilter
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


logger = logging.getLogger(__name__)

def index(request):
    logger.error('sa')
    posts = Post.objects.all()

    return render(request, 'posts.html', context={'posts': posts})

# class PostList(ListView):
#     model = Post
#     ordering = '-time_add'
#     template_name = 'posts.html'
#     context_object_name = 'posts'
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_author'] = self.request.user.groups.filter(name='authors').exists()
#         return context


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', kwargs={'pk':self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.comment_post = self.get_object()
        self.object.comment_user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(comment_post=post)
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_add'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def get_author_status(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(user)

    Author.objects.create(authorUser=User.objects.get(pk=user.id))
    return redirect('/news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category_post = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category_post=self.category_post).order_by('-time_add')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category_post.subscribers.all()
        context['category'] = self.category_post
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от рассылки новостей'
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})


# class CommentCreate(LoginRequiredMixin, CreateView):
#     raise_exception = True
#     form_class = CommentForm
#     model = Comment
#     template_name = 'comment_create.html'
#     success_url = reverse_lazy('post_list')
