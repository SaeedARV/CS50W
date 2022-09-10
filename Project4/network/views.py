from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Follow


def index(request):
    if request.method == "POST":
        Post.objects.create(
            poster=request.user,
            content=request.POST["newTextarea"],
        )
        return HttpResponseRedirect(reverse("index"))
    else:
        allPosts = Post.objects.all()

        paginator = Paginator(allPosts, 10)
        page_number = request.GET.get('page')
        allPosts_obj = paginator.get_page(page_number)
        
        return render(request, "network/index.html", {
            "page_obj": allPosts_obj
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
    try:
        user = User.objects.get(username=username)
    except:
        return render(request, "network/profilePage.html", {
            "message": "User not found."
        })

    isFollowed = False
    for follow in user.followed.all():
        if request.user == follow.follower:
            isFollowed = True

    paginator = Paginator(user.post.all(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profilePage.html", {
        "profileUser": user,
        "isFollowed": isFollowed,
        "page_obj": page_obj
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

def followingPosts(request):
    posts = Post.objects.all()
    followingPosts = []
    for post in posts:
        for follow in request.user.follower.all():
            if follow.followed == post.poster:
                followingPosts.append(post)


    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    followingPosts_obj = paginator.get_page(page_number)

    return render(request, "network/followingPosts.html", {
        "page_obj": followingPosts_obj
    })

@csrf_exempt
def editPost(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if(request.user.id == post.poster.id):
            content = request.POST["textarea"]

            post.content = content
            post.isEdited = True
            
            post.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=400)


