from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import (
    Post,
    PostLike,
    PostDislike
)

UserModel = get_user_model()


class PostImageSerializer(serializers.Serializer):
    """
    Serialize post image instance
    """
    def to_representation(self, value):
        request = self.context.get('request')
        return '%s' % request.build_absolute_uri(value.image.url)


class PostSerializer(serializers.Serializer):
    """
    Serialize post
    """
    created_on = serializers.DateTimeField()
    description = serializers.CharField()
    images = PostImageSerializer(many=True)  # related_name
    get_tags = serializers.CharField()

    like_post = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    dislike_post = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    post_liked_users = serializers.SerializerMethodField()

    def get_like_post(self, obj):
        kwargs = {
            'postid': obj.id,
        }
        url = reverse('post:likepost', kwargs=kwargs)
        return self.context['request'].build_absolute_uri(url)

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post=obj).count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        return PostLike.objects.filter(post__in=[obj], user=request.user).exists()

    def get_dislike_post(self, obj):
        kwargs = {
            'postid': obj.id,
        }
        url = reverse('post:dislikepost', kwargs=kwargs)
        return self.context['request'].build_absolute_uri(url)

    def get_dislikes_count(self, obj):
        return PostDislike.objects.filter(post=obj).count()

    def get_is_disliked(self, obj):
        request = self.context.get('request')
        return PostDislike.objects.filter(post__in=[obj], user=request.user).exists()

    def get_post_liked_users(self, obj):
        kwargs = {
            'postid': obj.id,
        }
        url = reverse('post:postlikedusers', kwargs=kwargs)
        return self.context['request'].build_absolute_uri(url)


class PostLikeSerializer(serializers.Serializer):
    """
    Serialize post like
    """
    user = serializers.StringRelatedField(read_only=True)