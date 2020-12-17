from django.db.models.aggregates import Case, When
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from posts.models import (
    Post,
    PostLike,
    PostDislike
)
from posts.serializers import (
    PostSerializer,
    PostLikeSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """
    View set for post model
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        liked_tags = []
        user = self.request.user
        for up in user.likedusers.all():
            for t in up.post.tags.all():
                liked_tags.append(t.id)
        return Post.objects.order_by(Case(When(tags__in=list(set(liked_tags)),then=0), default=1), "-tags__weight")


@api_view(('GET',))
@permission_classes([permissions.IsAuthenticated])
def like_post(request, postid):
    """
    View function for perform like
    """
    post = Post.objects.get(pk=postid)
    like, created = PostLike.objects.get_or_create(post=post,
                                                   user=request.user)
    PostDislike.objects.filter(post=post, user=request.user).delete()

    return Response({'details': 'liked'},
                    status=status.HTTP_200_OK)


@api_view(('GET',))
@permission_classes([permissions.IsAuthenticated])
def dislike_post(request, postid):
    """
    View function for perform dislike
    """
    post = Post.objects.get(pk=postid)
    dislike, created = PostDislike.objects.get_or_create(post=post,
                                                   user=request.user)
    PostLike.objects.filter(post=post, user=request.user).delete()

    return Response({'details': 'disliked post'},
                    status=status.HTTP_200_OK)


@api_view(('GET',))
@permission_classes([permissions.IsAuthenticated])
def post_liked_users(request, postid):
    """
    View function for get liked users per post
    """
    post = Post.objects.get(pk=postid)
    users = PostLike.objects.filter(post=post)
    serializer = PostLikeSerializer(users, many=True)

    return Response(serializer.data,
                    status=status.HTTP_200_OK)