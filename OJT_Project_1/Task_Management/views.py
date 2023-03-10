from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password

from .models import *

from datetime import *


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
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        idnum = request.POST.get('idnum')
        cnum = request.POST.get('cnum')
        email = request.POST.get('email')
        pic = request.FILES['pic']

        decrypted_pass = lname + '-' + idnum
        password = make_password(decrypted_pass)
        username = idnum

        position = "Employee"

        new_user = app_users.objects.create(username=username, password=password, first_name=fname, last_name=lname, email=email,
                                            id_number=idnum, contact_number=cnum, position=position, profile_pic=pic)
        new_user.save()
        return redirect("add_user")

    return render(request, 'html/Add_user.html')


def admin_add_task(request):
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        employees = request.POST.get('employees')
        categories = request.POST.get('categories')
        subcategories = request.POST.get('subcategories')
        stat = request.POST.get('stat')
        steps = request.POST.get('steps')

        published_date = date.today()

        new_task = tasks.objects.create(task_name=task_name, category=categories, subcategory=subcategories, details=steps,
                                        assigned_by="SAMPLE", assigned_to=employees, date_published=published_date,
                                        date_completed="NONE", status=stat)
        new_task.save()
        return redirect("admin_add_task")

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
