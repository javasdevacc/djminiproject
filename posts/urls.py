from django.urls import path, include, re_path
from rest_framework import routers
from posts import views

app_name = 'post'

router = routers.DefaultRouter()
router.register(r'post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^likepost/(?P<postid>\d+)/$', views.like_post, name='likepost'),
    re_path(r'^dislikepost/(?P<postid>\d+)/$', views.dislike_post, name='dislikepost'),
    re_path(r'^postlikedusers/(?P<postid>\d+)/$', views.post_liked_users, name='postlikedusers'),
]