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
    context = {"category_list": category_list}
    subcategory_list = subcategories.objects.all()
    context = {"category_list": category_list,
               "subcategory_list": subcategory_list}
    return render(request, 'html/Subcategory.html', context)


def steps(request):
    return render(request, 'html/Steps.html')

# Create your views here.


# for 2 forms submital
# def submit_form(request):
#     if request.method == 'POST':
#         if 'form1' in request.POST:
#             # process form1 data
#             # ...
#             return redirect('form1_success')
#         else:
#             # process form2 data
#             # ...
#             return redirect('form2_success')

#     # render the initial form page
#     return render(request, 'mytemplate.html')
