from django.db import models
from Posting.models import Post
from Users.models import User

# Create your models here.
class Like(models.Model):
    post_id = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_likes')
    username = models.ForeignKey(to=User, verbose_name='좋아요 한 사람', on_delete=models.CASCADE, related_name='user_likes')