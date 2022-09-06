from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

