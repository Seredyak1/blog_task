from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from .models import Blog, Post


@receiver(post_save, sender=User)
def create_blog_for_new_user(sender, created, instance, **kwargs):
    """Signal to create personal blog for new User"""
    if created:
        Blog.objects.create(user=instance)


@receiver(post_save, sender=Post)
def send_email(sender, instance, created, **kwargs):
    """Signal to send email to new Post"""
    if created:
        instance.notify_about_new_post()
