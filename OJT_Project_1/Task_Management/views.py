from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'html/Login_Page.html')


def client_home(request):
    return render(request, 'html/Client_dashboard_home.html')


def client_pending(request):
    return render(request, 'html/Client_dashboard_pending.html')


def client_complete(request):
    return render(request, 'html/Client_dashboard_complete.html')


def admin_home(request):
    return render(request, 'html/Admin_dashboard_home.html')


def admin_pending(request):
    return render(request, 'html/Admin_dashboard_pending.html')


def admin_complete(request):
    return render(request, 'html/Admin_dashboard_complete.html')


def admin_users(request):
    return render(request, 'html/Admin_dashboard_users.html')


def add_user(request):
    return render(request, 'html/Add_user.html')


def admin_add_task(request):
    return render(request, 'html/Admin_dashboard_add_task.html')


def admin_edit(request):
    return render(request, 'html/Admin_dashboard_edit.html')


def category(request):
    return render(request, 'html/Category.html')


def subcategory(request):
    return render(request, 'html/Subcategory.html')


def steps(request):
    return render(request, 'html/Steps.html')

# Create your views here.
