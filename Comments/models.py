from django.db import models
from Users.models import User 
from Posting.models import Post

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(to=Post, related_name="post_comments", on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, related_name="user_comments", on_delete=models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content