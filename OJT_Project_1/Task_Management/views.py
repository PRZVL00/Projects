from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password

from .models import *

from datetime import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            if user.position == "Employee":
                login(request, user)
                return redirect("client_home")
            else:
                login(request, user)
                return redirect("admin_home")
    return render(request, 'html/Login_Page.html')


@login_required(login_url='index')
def client_home(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Employee':
        if request.method == "POST":
            pass

        task_list = tasks.objects.filter(
            active_status="ON", assigned_to=full_name)
        total_active = task_list.count()
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list, "total_active": total_active,
                   "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Client_dashboard_home.html', context)
    else:
        return redirect("admin_home")


def complete_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    task.status = "Complete"
    task.date_completed = date.today()
    task.active_status = "DONE"
    task.save()
    return redirect('client_home')


@login_required(login_url='index')
def client_pending(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Employee':
        if request.method == "POST":
            pass

        task_list = tasks.objects.filter(
            active_status="OFF", assigned_to=full_name)
        total_pending = task_list.count()
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list, "total_pending": total_pending,
                   "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Client_dashboard_pending.html', context)
    else:
        return redirect("admin_home")


def accept_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    task.active_status = "ON"
    task.date_started = date.today()
    task.save()
    return redirect('client_pending')


@login_required(login_url='index')
def client_complete(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Employee':
        if request.method == "POST":
            pass

        task_list = tasks.objects.filter(
            active_status="DONE", assigned_to=full_name)
        total_complete = task_list.count()
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list, "total_complete": total_complete,
                   "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Client_dashboard_complete.html', context)
    else:
        return redirect("admin_home")


@login_required(login_url='index')
def admin_home(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        if request.method == "POST":
            pass
        task_list = tasks.objects.filter(
            active_status="ON")
        total_active = task_list.count()
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list,
                   "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_home.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def admin_pending(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        if request.method == "POST":
            pass

        the_pic = app_users.objects.get(username=username)
        task_list = tasks.objects.filter(active_status="OFF")
        context = {"task_list": task_list, "the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_pending.html', context)
    else:
        return redirect("client_home")


def delete_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    task.delete()
    return redirect('admin_pending')


@login_required(login_url='index')
def admin_complete(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        if request.method == "POST":
            pass

        task_list = tasks.objects.filter(
            active_status="DONE")
        total_complete = task_list.count()
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list,
                   "total_complete": total_complete, "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_complete.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def admin_users(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        the_pic = app_users.objects.get(username=username)
        context = {"the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_users.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def add_user(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
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

        the_pic = app_users.objects.get(username=username)
        context = {"the_pic": the_pic}
        return render(request, 'html/Add_user.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def admin_add_task(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
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
                                            date_completed="NONE", status=stat, active_status="OFF")
            new_task.save()
            return redirect("admin_add_task")

        employee_list = app_users.objects.filter(position="EMPLOYEE")
        category_list = categories.objects.all()
        subcategory_list = subcategories.objects.all()
        details_list = detail.objects.all()
        the_pic = app_users.objects.get(username=username)
        context = {"employee_list": employee_list, "category_list": category_list,
                   "subcategory_list": subcategory_list, "details_list": details_list, "the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_add_task.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def admin_edit(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':

        the_pic = app_users.objects.get(username=username)
        context = {"the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_edit.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def category(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
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
        the_pic = app_users.objects.get(username=username)
        context = {"category_list": category_list, "the_pic": the_pic}
        return render(request, 'html/Category.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def subcategory(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
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
        the_pic = app_users.objects.get(username=username)
        context = {"category_list": category_list,
                   "subcategory_list": subcategory_list, "the_pic": the_pic}
        return render(request, 'html/Subcategory.html', context)
    else:
        return redirect("client_home")


@login_required(login_url='index')
def steps(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        if request.method == "POST":
            if 'form1' in request.POST:
                cat_to_add = request.POST.get('cat_to_add')
                sub_to_add = request.POST.get('sub_to_add')
                new_details = request.POST.get('new_details')

                check_sub = detail.objects.filter(subcategory=sub_to_add)

                if check_sub.count() >= 1:
                    print(check_sub.count())
                else:
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
        the_pic = app_users.objects.get(username=username)
        context = {"category_list": category_list, "subcategory_list": subcategory_list,
                   "details_list": details_list, "the_pic": the_pic}
        return render(request, 'html/Steps.html', context)
    else:
        return redirect("client_home")


def logoutuser(request):
    logout(request)
    return redirect('index')
