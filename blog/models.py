from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    class Meta:
        ordering = ('-updated_at',)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='followed_blogs')

    def __str__(self):
        return str(self.user.first_name) + "'s" + " blog"


class Post(models.Model):
    class Meta:
        ordering = ('-updated_at',)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False, blank=False)
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_by = models.ManyToManyField(User, related_name='read_posts')

    def __str__(self):
        return self.title


