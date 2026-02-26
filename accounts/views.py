"""
Auth endpoints:
- register
- login (rate-limited to reduce brute-force)
- logout
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit

from .forms import RegisterForm


def register_view(request):
    """Register and log in a new user."""
    if request.user.is_authenticated:
        return redirect("/")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("/")

    return render(request, "accounts/register.html", {"form": form})


@ratelimit(key="ip", rate="10/m", block=True)
def login_view(request):
    """
    Log in view (rate-limited).
    Blocks excessive attempts per IP to mitigate brute-force.
    """
    if request.user.is_authenticated:
        return redirect("/")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next") or "/")

        error = "Invalid username or password."

    return render(request, "accounts/login.html", {"error": error})


@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect("/")