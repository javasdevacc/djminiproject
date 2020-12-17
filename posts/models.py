import time
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def post_img_url(instance, filename):
    hash_ = int(time.time())
    return "%s/%s_%s" % ("post", hash_, filename)


class Tag(models.Model):
    """
    To store tags of posts
    """
    name = models.CharField(max_length=100)
    weight = models.IntegerField()

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    To store post
    """
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500)
    tags = models.ManyToManyField(Tag, related_name='post')

    def __str__(self):
        return self.description[:15]

    def get_tags(self):
        return ",".join([t.name for t in self.tags.all()])

    @property
    def likes(self):
        return self.likedposts.all().count()

    @property
    def dislikes(self):
        return self.dislikedposts.all().count()


class Media(models.Model):
    """
    To store images of post
    """
    post = models.ForeignKey(
        Post,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        max_length=1000,
        upload_to=post_img_url
    )


class PostLike(models.Model):
    """
    To store post like
    """
    post = models.ForeignKey(
        Post,
        related_name='likedposts',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel,
        related_name='likedusers',
        on_delete=models.CASCADE
    )


class PostDislike(models.Model):
    """
    To store post dislike
    """
    post = models.ForeignKey(
        Post,
        related_name='dislikedposts',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel,
        related_name='dislikedusers',
        on_delete=models.CASCADE
    )