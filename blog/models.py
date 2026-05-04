from django.conf import settings
from django.db import models
from typing import TYPE_CHECKING
from django.utils.text import slugify

if TYPE_CHECKING:
    from django.db.models.manager import Manager


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    if TYPE_CHECKING:
        comments: "Manager[Comment]"

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    @property
    def comment_count(self) -> int:
        return self.comments.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} on Post #{self.post.pk}"


class PostReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    TYPES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="reactions"
    )
    reaction_type = models.CharField(max_length=10, choices=TYPES)

    class Meta:
        unique_together = ("user", "post")


class CommentReaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="reactions"
    )
    reaction_type = models.CharField(max_length=10, choices=PostReaction.TYPES)

    class Meta:
        unique_together = ("user", "comment")
