from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow


def index(request):
    if request.method == "POST":
        Post.objects.create(
            poster=request.user,
            content=request.POST["textarea"],
        )
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            posts = Post.objects.all()
            followingPosts = []
            for post in posts:
                for follow in request.user.follower.all():
                    if follow.followed == post.poster:
                        followingPosts.append(post)

            return render(request, "network/index.html", {
                "posts": posts,
                "followingPosts": followingPosts
            })
        else:
            return render(request, "network/index.html", {
                "posts": Post.objects.all()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profilePage(request, username):
    user = User.objects.get(username=username)
    isFollowed = False

    for follow in user.followed.all():
        if request.user == follow.follower:
            isFollowed = True

    return render(request, "network/profilePage.html", {
        "profileUser": user,
        "isFollowed": isFollowed
    })

def follow(request, profileUser_id):
    if request.method == "POST":
        profileUser = User.objects.get(id=profileUser_id)
        for follow in profileUser.followed.all():
            if request.user == follow.follower:
                Follow.objects.filter(follower=request.user).delete()
                break
        else:
            Follow.objects.create(
                follower=request.user,
                followed=profileUser
            )

        return HttpResponseRedirect(reverse("profilePage", args=[profileUser.username]))