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
        categ = request.POST.get('categories')
        subcateg = request.POST.get('subcategories')
        stat = request.POST.get('stat')
        the_details = request.POST.get('details')

        published_date = date.today()

        new_task = tasks.objects.create(task_name=task_name, category=categ, subcategory=subcateg, details=the_details,
                                        assigned_by="SAMPLE", assigned_to=employees, date_published=published_date,
                                        date_completed="NONE", status=stat)
        new_task.save()
        return redirect("admin_add_task")

    employee_list = app_users.objects.filter(position="EMPLOYEE")
    category_list = categories.objects.all()
    subcategory_list = subcategories.objects.all()
    details_list = detail.objects.all()
    context = {"employee_list": employee_list, "category_list": category_list,
               "subcategory_list": subcategory_list, "details_list": details_list}
    return render(request, 'html/Admin_dashboard_add_task.html', context)


def admin_edit(request):
    return render(request, 'html/Admin_dashboard_edit.html')


def category(request):
    if request.method == "POST":
        if 'form1' in request.POST:
            ncat = request.POST.get('ncat')

            new_category = categories.objects.create(category=ncat.upper())
            new_category.save()
            return redirect("category")

        else:
            dcat = request.POST.get('dcat')

            selected_category = categories.objects.get(category=dcat)
            selected_category.delete()
            return redirect('category')

    category_list = categories.objects.all()
    context = {"category_list": category_list}
    return render(request, 'html/Category.html', context)


def subcategory(request):
    if request.method == "POST":
        if 'form1' in request.POST:
            cat_add = request.POST.get('cat_add')
            nsubcat = request.POST.get('nsubcat')

            new_subcategory = subcategories.objects.create(
                category=cat_add, subcategory=nsubcat.upper())
            new_subcategory.save()
            return redirect("subcategory")

        else:
            cat_del = request.POST.get('cat_del')
            dsubcat = request.POST.get('dsubcat')

            selected_subcategory = subcategories.objects.get(
                category=cat_del, subcategory=dsubcat)
            selected_subcategory.delete()
            return redirect('subcategory')

    category_list = categories.objects.all()
    subcategory_list = subcategories.objects.all()
    context = {"category_list": category_list,
               "subcategory_list": subcategory_list}
    return render(request, 'html/Subcategory.html', context)


def steps(request):
    if request.method == "POST":
        if 'form1' in request.POST:
            cat_to_add = request.POST.get('cat_to_add')
            sub_to_add = request.POST.get('sub_to_add')
            new_details = request.POST.get('new_details')

            new_step = detail.objects.create(
                category=cat_to_add, subcategory=sub_to_add, details=new_details)
            new_step.save()
            return redirect("steps")

        elif 'form2' in request.POST:
            detail_to_del = request.POST.get('sub_to_del')

            selected_detail = detail.objects.get(
                subcategory=detail_to_del)
            selected_detail.delete()
            return redirect('steps')

        elif 'form3' in request.POST:
            detail_to_up = request.POST.get('sub_to_up')
            new_details = request.POST.get('new_details')

            selected_detail = detail.objects.get(
                subcategory=detail_to_up)
            selected_detail.details = new_details
            selected_detail.save()
            return redirect('steps')

    category_list = categories.objects.all()
    subcategory_list = subcategories.objects.all()
    details_list = detail.objects.all()
    context = {"category_list": category_list,
               "subcategory_list": subcategory_list,
               "details_list": details_list}
    return render(request, 'html/Steps.html', context)
