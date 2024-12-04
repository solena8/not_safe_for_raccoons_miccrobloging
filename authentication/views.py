from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


def logout_user(request):
    logout(request)
    return redirect('login')
