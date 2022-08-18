from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    imgURL = models.CharField(max_length=1000)
    category = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)


class Bids(models.Model):
    list = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name='bid')
    price = models.IntegerField()


class Comments(models.Model):
    list = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
