from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView

from .models import Blog, Post


class AuthenticatedMixin(object):
    """Mixin, check in user's auth.
    If not - redirect ot url"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login/')
        return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)


class NewsLineView(AuthenticatedMixin, generic.ListView):
    """
    get:
    Show all posts from blog, what user follow. Exclude himself
    """
    template_name = 'blog/newsline.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(blog__followers=user).exclude(user=user)
        return queryset


class PostDetailView(AuthenticatedMixin, generic.DetailView):
    """
    get:
    Show post detail by pk
    """
    template_name = 'blog/post_detail.html'
    model = Post


class NewsPostView(AuthenticatedMixin, CreateView):
    """
    post:
    Create news post
    """
    template_name = 'blog/posts_new.html'
    queryset = Post.objects.all()
    fields = ('title', 'body')
    success_url = reverse_lazy('blogs_my')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.blog = self.request.user.blog
        return super().form_valid(form)


class PostDeleteView(AuthenticatedMixin, DeleteView):
    """
    Delete post.
    get: Use for delete without confirm
    """
    model = Post
    success_url = reverse_lazy('blogs_my')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class MarkPostAsReadView(AuthenticatedMixin, View):
    """
    get:
    Mark post as read. Add user to field "read_by"
    """
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.read_by.add(request.user)
        messages.success(request, "Post {} by {} is read!".format(post.pk, post.user))
        return redirect('newsline')


class MarkPostAsUnread(AuthenticatedMixin, View):
    """
    get:
    Mark post as unread. Remove user from field "read_by"
    """
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.read_by.remove(request.user)
        messages.error(request, "Post {} by {} is unread!".format(post.pk, post.user))
        return redirect('newsline')


class MyBlogView(AuthenticatedMixin, generic.ListView):
    """
    get:
    Show all user's post.
    """
    template_name = 'blog/blogs_my.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class BlogsListView(AuthenticatedMixin, generic.ListView):
    """
    get:
    Show all blogs, available for following without user's blog
    """
    template_name = 'blog/blogs_list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.all().exclude(user=self.request.user)


class BlogDetailView(AuthenticatedMixin, View):
    """
    get:
    Show all posts and blog's detail, created by another user
    """
    paginate_by = 10

    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        posts = Post.objects.filter(blog=blog)
        return render(request, 'blog/blogs_detail.html', {'blog': blog,
                                                         'posts': posts})


class FollowToBlogView(AuthenticatedMixin, View):
    """
    get:
    Start to "follow" from another blog; Add user to field "followers"
    """
    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        blog.followers.add(request.user.id)
        messages.success(request, "You follow to {}".format(blog.user))
        return redirect('blogs_list')


class UnfollowFromBlogView(AuthenticatedMixin, View):
    """
    get:
    Stop to "follow" from another blog:
    Remuve user from field "followers" and from filed "read_by" in Post
    """
    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=pk)
        blog.followers.remove(request.user.id)
        for post in Post.objects.filter(blog=blog):
            post.read_by.remove(request.user.id)
        messages.error(request, "You don't follow to {}".format(blog.user))
        return redirect('blogs_list')
