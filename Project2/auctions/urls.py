from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listingPage/<int:listing_id>", views.listingPage, name="listingPage"),
    path("addToWatchlist/<int:listing_id>", views.addToWatchlist, name="addToWatchlist"),
    path("newBid/<int:listing_id>", views.newBid, name="newBid"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment")
]
