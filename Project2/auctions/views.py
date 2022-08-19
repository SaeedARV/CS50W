from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, AuctionListings, Bids, Comments


class listingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1000)
    startingBid = forms.IntegerField(label='Starting Bid', min_value=0)
    imgURL = forms.CharField(
        label='image URL', max_length=1000, required=False)
    category = forms.CharField(max_length=64, required=False)


def index(request):
    bids = []
    for auction in AuctionListings.objects.all():
        bids.append(auction.bid.get().price)

    return render(request, "auctions/index.html", {
        "AuctionListings": zip(bids, AuctionListings.objects.all()),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]
        imgURL = request.POST["imgURL"]
        category = request.POST["category"]

        list = AuctionListings.objects.create(
            user=request.user,
            title=title,
            description=description,
            imgURL=imgURL,
            category=category,
        )

        Bids.objects.create(
            list=list,
            person=request.user,
            price=startingBid,
        )

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createListing.html", {
            "form": listingForm()
        })

def listingPage(request, listing_id):
    if request.method == "GET":
        auction = AuctionListings.objects.get(id=listing_id)
        creator = False
        if request.user == auction.user:
            creator = True

        bid = auction.bid.get()

        return render(request, "auctions/listingPage.html", {
            "creator": creator,
            "auction": auction,
            "bid": bid,
        })

def addToWatchlist(request, listing_id):
    if request.method == "POST":
        auction = AuctionListings.objects.get(id=listing_id)
        if auction in request.user.watchlist.all():
            request.user.watchlist.remove(auction)
        else:
            request.user.watchlist.add(auction)

        return HttpResponseRedirect(reverse("listingPage", args=[listing_id]))
    else:
        return HttpResponseRedirect(reverse("listingPage", args=[listing_id]))

def newBid(request, listing_id):
    if request.method == "POST":
        newBid = request.POST["newBid"]
        auction = AuctionListings.objects.get(id=listing_id)
        auction.bid.update(price=newBid)
        auction.bid.update(person=request.user)

        return HttpResponseRedirect(reverse("listingPage", args=[listing_id]))
    else:
        return HttpResponseRedirect(reverse("listingPage", args=[listing_id]))

def closeAuction(request, listing_id):
    if request.method == "POST":
        auction = AuctionListings.objects.get(id=listing_id)
        auction.isActive=False
        auction.save()

        return HttpResponseRedirect(reverse("listingPage", args=[listing_id]))
    else:
        return HttpResponseRedirect(reverse("listingPage", args=[listing_id]))