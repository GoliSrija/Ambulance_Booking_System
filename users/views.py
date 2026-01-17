from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile


# -----------------------
# LOGIN
# -----------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "users/login.html", {
                "error": "Please enter both username and password"
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("users:dashboard")
        else:
            return render(request, "users/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "users/login.html")


# -----------------------
# DASHBOARD
# -----------------------
@login_required(login_url="users:login")
def dashboard(request):
    return render(request, "users/dashboard.html")


# -----------------------
# LOGOUT
# -----------------------
@login_required(login_url="users:login")
def logout_view(request):
    logout(request)
    return redirect("users:login")


# -----------------------
# REGISTER (PATIENT ONLY)
# -----------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "users/register.html", {
                "error": "All fields are required"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "users/register.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ✅ Default role: PATIENT
        Profile.objects.create(
            user=user,
            role="patient"
        )

        return redirect("users:login")

    return render(request, "users/register.html")
