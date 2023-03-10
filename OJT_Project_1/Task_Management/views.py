from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'html/Login_Page.html')


def client_home(request):
    return render(request, 'html/Client_dashboard_home.html')


def client_pending(request):
    return render(request, 'html/Client_dashboard_pending.html')

# Create your views here.
