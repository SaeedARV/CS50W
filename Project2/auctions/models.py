from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField()
    description = models.CharField()
    imgURL = models.CharField()
    category = models.CharField()

class Bids(models.Model):
    list = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    price = models.IntegerField()

class Comments(models.Model):
    list = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    text = models.CharField()
