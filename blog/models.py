from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail


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

    def notify_about_new_post(self):
        users_email = self.blog.followers.values_list('email', flat=True)
        subject = 'In Blog we have new post!'
        html_content = 'You can look it here: http://127.0.0.1:8000/posts/{}/'.format(self.pk)
        send_mail(subject, html_content, 'laik.travel@gmail.com', users_email, fail_silently=True)
