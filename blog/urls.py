from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NewsLineView.as_view(), name='newsline'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^posts/(?P<pk>[0-9]+)/mark_as_read/$', views.MarkPostAsReadView.as_view(), name='post_read'),
    url(r'^posts/(?P<pk>[0-9]+)/mark_as_unread/$', views.MarkPostAsUnread.as_view(), name='post_unread'),
    url(r'^posts/new/$', views.NewsPostView.as_view(), name='post_new'),
    url(r'^posts/(?P<pk>[0-9]+)/delete/$', views.PostDeleteView.as_view(), name='post_delete'),
    url(r'^blogs/$', views.BlogsListView.as_view(), name='blogs_list'),
    url(r'^blogs/my/$', views.MyBlogView.as_view(), name='blogs_my'),
    url(r'^blogs/(?P<pk>[0-9]+)/$', views.BlogDetailView.as_view(), name='blogs_detail'),
    url(r'^blog/(?P<pk>[0-9]+)/follow/', views.FollowToBlogView.as_view(), name='follow'),
    url(r'^blog/(?P<pk>[0-9]+)/disfollow/', views.DisfollowFromBlogView.as_view(), name='disfollow'),
]
