from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def register_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:register")

        if User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect("accounts:register")

        user = User.objects.create_user(phone_number=phone, email=email, password=password)
        messages.success(request, "Account created. You can log in now.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone_number")
        password = request.POST.get("password")
        user = authenticate(request, phone_number=phone, password=password)
        if user:
            login(request, user)
            return redirect("farms:home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
