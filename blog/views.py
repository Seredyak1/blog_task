from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView

from .models import Blog, Post


class AuthenticatedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login/')
        return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)


class NewsLineView(AuthenticatedMixin, generic.ListView):

    template_name = 'blog/newsline.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(blog__followers=user).exclude(user=user)
        return queryset


class PostDetailView(AuthenticatedMixin, generic.DetailView):

    template_name = 'blog/post_detail.html'
    model = Post


class NewsPostView(AuthenticatedMixin, CreateView):

    template_name = 'blog/posts_new.html'
    queryset = Post.objects.all()
    fields = ('title', 'body')
    success_url = reverse_lazy('blogs_my')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.blog = self.request.user.blog
        return super().form_valid(form)


class PostDeleteView(AuthenticatedMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blogs_my')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class MarkPostAsReadView(AuthenticatedMixin, View):

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.read_by.add(request.user)
        messages.success(request, "Post {} by {} is read!".format(post.pk, post.user))
        return redirect('newsline')


class MarkPostAsUnread(AuthenticatedMixin, View):

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.read_by.remove(request.user)
        messages.error(request, "Post {} by {} is unread!".format(post.pk, post.user))
        return redirect('newsline')


class MyBlogView(AuthenticatedMixin, generic.ListView):

    template_name = 'blog/blogs_my.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class BlogsListView(AuthenticatedMixin, generic.ListView):

    template_name = 'blog/blogs_list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.all().exclude(user=self.request.user)


class BlogDetailView(AuthenticatedMixin, View):

    paginate_by = 10

    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        posts = Post.objects.filter(blog=blog)
        return render(request, 'blog/blogs_detail.html', {'blog': blog,
                                                         'posts': posts})


class FollowToBlogView(AuthenticatedMixin, View):
    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        blog.followers.add(request.user.id)
        messages.success(request, "You follow to {}".format(blog.user))
        return redirect('blogs_list')


class DisfollowFromBlogView(AuthenticatedMixin, View):
    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        blog.followers.remove(request.user.id)
        for post in Post.objects.filter(blog=blog):
            post.read_by.remove(request.user.id)
        messages.error(request, "You don't follow to {}".format(blog.user))
        return redirect('blogs_list')
