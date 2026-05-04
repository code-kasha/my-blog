from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, UserUpdateForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("post_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created")
            return redirect("post_list")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "users/profile.html")


@login_required
def update_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "users/update_profile.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
