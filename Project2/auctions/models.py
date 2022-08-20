from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    imgURL = models.CharField(max_length=5000)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    Watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    date = models.DateTimeField(default=timezone.now)


class Bids(models.Model):
    list = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name='bid')
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()


class Comments(models.Model):
    list = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comment")
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000)
    date = models.DateTimeField(default=timezone.now)
