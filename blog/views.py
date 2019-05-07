from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

from .models import Blog, Post


class NewsLineView(generic.ListView):

    template_name = 'blog/newsline.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(blog__followers=user).exclude(user=user)
        return queryset


class PostDetailView(generic.DetailView):

    template_name = 'blog/post_detail.html'
    model = Post


class MyBlogView(generic.ListView):

    template_name = 'blog/blogs_my.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class BlogsListView(generic.ListView):

    template_name = 'blog/blogs_list.html'
    context_object_name = 'blogs'
    paginate_by = 20

    def get_queryset(self):
        return Blog.objects.all().exclude(user=self.request.user)


class BlogDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        posts = Post.objects.filter(blog=blog)
        return render(request, 'blog/blogs_detail.html', {'blog': blog,
                                                         'posts': posts})
