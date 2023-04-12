from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password

from .models import *

from datetime import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.db.models import Q
from django.core.mail import send_mail

from datetime import *


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            if user.position == "Employee":
                login(request, user)

                today = date.today()
                date_today = today.strftime("%Y-%m-%d")
                the_user = app_users.objects.get(username=username)

                now = datetime.now()
                current_time = now.strftime("%H:%M")

                the_log = logbook.objects.filter(
                    name=the_user.full_name, date_logged=date_today).count()

                if the_log == 0:

                    log_time = logbook.objects.create(name=the_user.full_name, id_number=the_user.id_number,
                                                      date_logged=date_today, time_logged=current_time, time_logged_out="NTO")
                    log_time.save()
                    return redirect("client_home")

                else:
                    return redirect("client_home")
            else:
                login(request, user)

                today = date.today()
                date_today = today.strftime("%Y-%m-%d")
                the_user = app_users.objects.get(username=username)

                now = datetime.now()
                current_time = now.strftime("%H:%M")

                the_log = logbook.objects.filter(
                    name=the_user.full_name, date_logged=date_today).count()

                if the_log == 0:

                    log_time = logbook.objects.create(name=the_user.full_name, id_number=the_user.id_number,
                                                      date_logged=date_today, time_logged=current_time, time_logged_out="NTO")
                    log_time.save()
                    return redirect("client_home")

                else:
                    return redirect("client_home")

    return render(request, 'html/Login_Page.html')


@login_required(login_url='index')
def client_home(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Employee':
        if request.method == "POST":
            item = request.POST.get("search_bar")

            task_list = tasks.objects.filter(
                Q(id__icontains=item, active_status="ON", assigned_to=full_name) |
                Q(task_name__icontains=item, active_status="ON", assigned_to=full_name) |
                Q(category__icontains=item, active_status="ON", assigned_to=full_name) |
                Q(subcategory__icontains=item, active_status="ON", assigned_to=full_name) |
                Q(assigned_by__icontains=item, active_status="ON", assigned_to=full_name) |
                Q(assigned_to__icontains=item,
                  active_status="ON", assigned_to=full_name)
            ).order_by("-id")

            total_active = task_list.count()
            the_user = full_name
            the_pic = app_users.objects.get(username=username)
            context = {"task_list": task_list, "total_active": total_active,
                       "the_user": the_user, "the_pic": the_pic}
            return render(request, 'html/Client_dashboard_home.html', context)

######################################################################################
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        task_list2 = tasks.objects.filter(
            active_status="ON", assigned_to=full_name).order_by("-id")

        for the_task_list in task_list2:
            task_history_list = task_history.objects.filter(
                task_id=the_task_list.task_id, status="ACTIVE")

            for num_hours in task_history_list:

                time1 = datetime.strptime(
                    num_hours.time_continued, '%H:%M').time()
                time2 = datetime.strptime(current_time, '%H:%M').time()
                diff = datetime.combine(
                    datetime.today(), time2) - datetime.combine(datetime.today(), time1)
                diff_minutes = round(diff.total_seconds() / 3600, 2)

                num_hours.man_hours = diff_minutes
                num_hours.save()

        base_ttl = 0

        for the_task_list2 in task_list2:
            task_history_list = task_history.objects.filter(
                task_id=the_task_list2.task_id)
            print(str(task_history_list.count()))

            for num_hours2 in task_history_list:
                base_ttl += float(num_hours2.man_hours)

                print(base_ttl)

                ttl_hrs = (base_ttl - float(the_task_list2.total_hours)
                           ) + float(the_task_list2.total_hours)

                the_task_list2.total_hours = round(ttl_hrs, 2)
                the_task_list2.save()


######################################################################################
        task_list = tasks.objects.filter(
            active_status__in=["ON", "PAUSED"], assigned_to=full_name).order_by("-id")
        the_user = full_name
        total_active = task_list.count()
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list, "total_active": total_active,
                   "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Client_dashboard_home.html', context)
    else:
        return redirect("admin_home")


def complete_task(request, task_id):
    username = request.user.username

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    task = tasks.objects.get(task_id=task_id)
    task.status = "Complete"
    task.date_completed = date.today()
    task.active_status = "DONE"
    task.time_completed = current_time
    task.save()

    full_name = app_users.objects.get(username=username)
    active_task_count = tasks.objects.filter(
        assigned_to=full_name.full_name, active_status="ON").count()
    pending_task_count = tasks.objects.filter(
        assigned_to=full_name.full_name, active_status="OFF").count()

    full_name.active_task_count = active_task_count
    full_name.pending_task_count = pending_task_count
    full_name.save()

    ttl_hrs = 0

    count_hrs = task_history.objects.filter(task_id=task_id)
    for man_hrs in count_hrs:
        ttl_hrs += float(man_hrs.man_hours)
        task.total_hours = round(ttl_hrs, 2)

    send_mail(
        task.task_name + ' Finished',
        'Task ID ' + str(task.task_id) + " with a task name of " +
        task.task_name + ", was finished by " + task.assigned_to + " with a date stamp of " +
        str(date.today()) + ".",
        'rsb.taskmanagement@gmail.com',
        ["josiahbautista00@gmail.com"],)
    return redirect('client_home')


def pause_task(request, task_id):
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    task = tasks.objects.get(task_id=task_id)
    task.status = "Paused"
    task.active_status = "PAUSED"
    task.save()

    the_task_history = task_history.objects.filter(
        task_id=task_id, status="ACTIVE").latest('id')
    the_task_history.time_paused = current_time
    the_task_history.status = "Paused"
    the_task_history.save()
    return redirect('client_home')


def continue_task(request, task_id):
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    task = tasks.objects.get(task_id=task_id)
    task.status = "Active"
    task.active_status = "ON"
    task.save()

    new_task_history = task_history.objects.create(task_id=task.task_id, date=date.today(
    ), time_continued=current_time, time_paused="N/A", man_hours="0", status="Active")
    new_task_history.save()

    return redirect('client_home')


@login_required(login_url='index')
def client_pending(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Employee':
        if request.method == "POST":
            item = request.POST.get("search_bar")

            task_list = tasks.objects.filter(
                Q(id__icontains=item, active_status="OFF", assigned_to=full_name) |
                Q(task_name__icontains=item, active_status="OFF", assigned_to=full_name) |
                Q(category__icontains=item, active_status="OFF", assigned_to=full_name) |
                Q(subcategory__icontains=item, active_status="OFF", assigned_to=full_name) |
                Q(assigned_by__icontains=item, active_status="OFF", assigned_to=full_name) |
                Q(assigned_to__icontains=item,
                  active_status="OFF", assigned_to=full_name)
            ).order_by("-id")

            total_pending = task_list.count()
            the_user = full_name
            the_pic = app_users.objects.get(username=username)
            context = {"task_list": task_list, "total_pending": total_pending,
                       "the_user": the_user, "the_pic": the_pic}
            return render(request, 'html/Client_dashboard_pending.html', context)

        task_list = tasks.objects.filter(
            active_status="OFF", assigned_to=full_name).order_by("-id")
        total_pending = task_list.count()
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"task_list": task_list, "total_pending": total_pending,
                   "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Client_dashboard_pending.html', context)
    else:
        return redirect("admin_home")


def accept_task(request, task_id):
    username = request.user.username

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    task = tasks.objects.get(id=task_id)
    task.active_status = "ON"
    task.date_started = date.today()
    task.time_started = current_time
    task.total_hours = "0"
    task.save()

    new_task_history = task_history.objects.create(task_id=task.task_id, date=date.today(
    ), time_continued=current_time, time_paused="N/A", man_hours="0", status="ACTIVE")
    new_task_history.save()

    full_name = app_users.objects.get(username=username)
    active_task_count = tasks.objects.filter(
        assigned_to=full_name.full_name, active_status="ON").count()
    pending_task_count = tasks.objects.filter(
        assigned_to=full_name.full_name, active_status="OFF").count()

    full_name.active_task_count = active_task_count
    full_name.pending_task_count = pending_task_count
    full_name.save()

    send_mail(
        "" + task.task_name + 'Started',
        'Task number ' + str(task.id) + " with a task name of " +
        task.task_name + ", was started by " + task.assigned_to + " with a date stamp of " +
        str(date.today()) + ".",
        'rsb.taskmanagement@gmail.com',
        ["josiahbautista00@gmail.com"],)

    return redirect('client_pending')


@login_required(login_url='index')
def client_complete(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Employee':
        if request.method == "POST":
            item = request.POST.get("search_bar")

            task_list = tasks.objects.filter(
                Q(id__icontains=item, active_status="DONE", assigned_to=full_name) |
                Q(task_name__icontains=item, active_status="DONE", assigned_to=full_name) |
                Q(category__icontains=item, active_status="DONE", assigned_to=full_name) |
                Q(subcategory__icontains=item, active_status="DONE", assigned_to=full_name) |
                Q(assigned_by__icontains=item, active_status="DONE", assigned_to=full_name) |
                Q(assigned_to__icontains=item,
                  active_status="DONE", assigned_to=full_name)
            ).order_by("-id")

            total_complete = task_list.count()
            the_user = full_name
            the_pic = app_users.objects.get(username=username)
            context = {"task_list": task_list, "total_complete": total_complete,
                       "the_user": the_user, "the_pic": the_pic}
            return render(request, 'html/Client_dashboard_complete.html', context)

        task_list = tasks.objects.filter(
            active_status="DONE", assigned_to=full_name).order_by("-id")
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
            if 'general_search' in request.POST:
                # the item that is searched
                item = request.POST.get("search_bar")

                task_list = tasks.objects.filter(
                    Q(id__icontains=item, active_status="ON") |
                    Q(task_name__icontains=item, active_status="ON") |
                    Q(category__icontains=item, active_status="ON") |
                    Q(subcategory__icontains=item, active_status="ON") |
                    Q(assigned_by__icontains=item, active_status="ON") |
                    Q(assigned_to__icontains=item, active_status="ON")
                ).order_by("-id")

                total_active = task_list.count()
                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"task_list": task_list,
                           "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_home.html', context)\

            elif 'date_search' in request.POST:
                date_category = request.POST.get("tvalue_date_category")
                from_date = request.POST.get("tvalue_from_date")
                to_date = request.POST.get("tvalue_to_date")

                if date_category == "Date Published":
                    task_list = tasks.objects.filter(
                        date_published__range=(from_date, to_date), active_status="ON").order_by("-id")
                    total_active = task_list.count()
                    the_user = full_name
                    the_pic = app_users.objects.get(username=username)
                    context = {"task_list": task_list,
                               "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                    return render(request, 'html/Admin_dashboard_home.html', context)

                elif date_category == "Date Started":
                    task_list = tasks.objects.filter(
                        date_started__range=(from_date, to_date), active_status="ON").order_by("-id")
                    total_active = task_list.count()
                    the_user = full_name
                    the_pic = app_users.objects.get(username=username)
                    context = {"task_list": task_list,
                               "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                    return render(request, 'html/Admin_dashboard_home.html', context)

#########################################################################################

        now = datetime.now()
        current_time = now.strftime("%H:%M")

        task_list2 = tasks.objects.filter(
            active_status="ON").order_by("-id")

        for the_task_list in task_list2:
            task_history_list = task_history.objects.filter(
                task_id=the_task_list.task_id, status="ACTIVE")

            for num_hours in task_history_list:

                time1 = datetime.strptime(
                    num_hours.time_continued, '%H:%M').time()
                time2 = datetime.strptime(current_time, '%H:%M').time()
                diff = datetime.combine(
                    datetime.today(), time2) - datetime.combine(datetime.today(), time1)
                diff_minutes = round(diff.total_seconds() / 3600, 2)

                num_hours.man_hours = diff_minutes
                num_hours.save()

        base_ttl = 0

        for the_task_list2 in task_list2:
            task_history_list = task_history.objects.filter(
                task_id=the_task_list2.task_id)
            print(str(task_history_list.count()))

            for num_hours2 in task_history_list:
                base_ttl += float(num_hours2.man_hours)

                print(base_ttl)

                ttl_hrs = (base_ttl - float(the_task_list2.total_hours)
                           ) + float(the_task_list2.total_hours)

                the_task_list2.total_hours = round(ttl_hrs, 2)
                the_task_list2.save()

#########################################################################################

        task_list = tasks.objects.filter(
            active_status="ON").order_by("-id")
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
            if 'general_search' in request.POST:
                # the item that is searched
                item = request.POST.get("search_bar")

                task_list = tasks.objects.filter(
                    Q(id__icontains=item, active_status="OFF") |
                    Q(task_name__icontains=item, active_status="OFF") |
                    Q(category__icontains=item, active_status="OFF") |
                    Q(subcategory__icontains=item, active_status="OFF") |
                    Q(assigned_by__icontains=item, active_status="OFF") |
                    Q(assigned_to__icontains=item, active_status="OFF")
                ).order_by("-id")

                total_active = task_list.count()
                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"task_list": task_list,
                           "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_pending.html', context)

            elif 'date_search' in request.POST:
                from_date = request.POST.get("tvalue_from_date")
                to_date = request.POST.get("tvalue_to_date")

                task_list = tasks.objects.filter(
                    date_published__range=(from_date, to_date), active_status="OFF").order_by("-id")
                total_active = task_list.count()
                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"task_list": task_list,
                           "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_pending.html', context)

        the_pic = app_users.objects.get(username=username)
        task_list = tasks.objects.filter(active_status="OFF").order_by("-id")
        context = {"task_list": task_list, "the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_pending.html', context)
    else:
        return redirect("client_home")


def delete_task(request, task_id):
    task = tasks.objects.get(id=task_id)
    task.delete()

    full_name = app_users.objects.get(full_name=task.assigned_to)
    active_task_count = tasks.objects.filter(
        assigned_to=full_name.full_name, active_status="ON").count()
    pending_task_count = tasks.objects.filter(
        assigned_to=full_name.full_name, active_status="OFF").count()
    full_name.active_task_count = active_task_count
    full_name.pending_task_count = pending_task_count
    full_name.save()
    return redirect('admin_pending')


@login_required(login_url='index')
def admin_complete(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        if request.method == "POST":
            if 'general_search' in request.POST:
                # the item that is searched
                item = request.POST.get("search_bar")

                task_list = tasks.objects.filter(
                    Q(id__icontains=item, active_status="DONE") |
                    Q(task_name__icontains=item, active_status="DONE") |
                    Q(category__icontains=item, active_status="DONE") |
                    Q(subcategory__icontains=item, active_status="DONE") |
                    Q(assigned_by__icontains=item, active_status="DONE") |
                    Q(assigned_to__icontains=item, active_status="DONE")
                ).order_by("-id")

                total_active = task_list.count()
                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"task_list": task_list,
                           "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_complete.html', context)

            elif 'date_search' in request.POST:
                from_date = request.POST.get("tvalue_from_date")
                to_date = request.POST.get("tvalue_to_date")

                task_list = tasks.objects.filter(
                    date_published__range=(from_date, to_date), active_status="DONE").order_by("-id")
                total_active = task_list.count()
                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"task_list": task_list,
                           "total_active": total_active, "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_complete.html', context)

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
        if request.method == "POST":
            item = request.POST.get("search_bar")

            employee_list = app_users.objects.filter(
                Q(first_name__icontains=item, position="Employee") |
                Q(last_name__icontains=item, position="Employee") |
                Q(email__icontains=item, position="Employee") |
                Q(id_number__icontains=item, position="Employee") |
                Q(contact_number__icontains=item, position="Employee") |
                Q(full_name__icontains=item, position="Employee")).order_by("-id_number")

            the_pic = app_users.objects.get(username=username)
            context = {"the_pic": the_pic, "employee_list": employee_list}
            return render(request, 'html/Admin_dashboard_users.html', context)

        employee_list = app_users.objects.filter(
            position="Employee").order_by("-id_number")
        the_pic = app_users.objects.get(username=username)
        context = {"the_pic": the_pic,
                   "employee_list": employee_list}
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

            full_name = fname + " " + lname

            existing_user = app_users.objects.filter(id_number=idnum).count()

            if existing_user >= 1:
                messages.error(request,  idnum + ' is already existing.')
                return redirect("add_user")

            else:
                new_user = app_users.objects.create(username=username, password=password, first_name=fname,
                                                    last_name=lname, email=email, id_number=idnum,
                                                    contact_number=cnum, position=position, profile_pic=pic,
                                                    full_name=full_name, active_task_count=0, pending_task_count=0)
                new_user.save()

                send_mail(
                    'Test Run for Registration',
                    'Good Day! You are now registered on RSB Task Management System. For your authentication, use your Id number as your username (RSB-XXXX) and combination of last name and id (Surname-RSB-XXXX). You can access your account in this website (Future link here).',
                    'rsb.taskmanagement@gmail.com',
                    [email],)
                messages.success(request,  idnum + ' was created succesfully.')
                return redirect("add_user")

        the_pic = app_users.objects.get(username=username)
        context = {"the_pic": the_pic}
        return render(request, 'html/Add_user.html', context)
    else:
        return redirect("client_home")


def delete_user(request, employees_id):
    user = app_users.objects.get(id=employees_id)
    the_tasks = tasks.objects.filter(
        active_status__in=["ON", "OFF"], assigned_to=user.full_name)
    the_tasks.delete()
    user.delete()
    return redirect('admin_users')


@login_required(login_url='index')
def admin_logbook(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username
    if request.user.is_authenticated and request.user.position == 'Admin':
        if request.method == "POST":
            if 'general_search' in request.POST:
                # the item that is searched
                item = request.POST.get("search_bar")

                log_list = logbook.objects.filter(
                    Q(id_number__icontains=item) |
                    Q(name__icontains=item) |
                    Q(time_logged__icontains=item)
                ).order_by("-id")

                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"log_list": log_list,
                           "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_logbook.html', context)\

            elif 'date_search' in request.POST:
                from_date = request.POST.get("tvalue_from_date")
                to_date = request.POST.get("tvalue_to_date")

                log_list = logbook.objects.filter(
                    date_logged__range=(from_date, to_date)).order_by("-id")
                the_user = full_name
                the_pic = app_users.objects.get(username=username)
                context = {"log_list": log_list,
                           "the_user": the_user, "the_pic": the_pic}
                return render(request, 'html/Admin_dashboard_logbook.html', context)

        today = date.today()
        date_today = today.strftime("%Y-%m-%d")
        log_list = logbook.objects.filter(
            date_logged=str(date_today)).order_by("-id")
        the_user = full_name
        the_pic = app_users.objects.get(username=username)
        context = {"log_list": log_list,
                   "the_user": the_user, "the_pic": the_pic}
        return render(request, 'html/Admin_dashboard_logbook.html', context)
    else:
        return redirect("client_logbook")


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
                                            assigned_by=full_name, assigned_to=employees, date_published=published_date,
                                            date_completed="NONE", status=stat, active_status="OFF")
            new_task.save()

            latest_task = tasks.objects.latest("id")
            latest_task.task_id = "RSB-T-" + str(latest_task.id)
            latest_task.save()

            the_pending_task_count = tasks.objects.filter(
                active_status="OFF", assigned_to=employees).count()
            add_pending_task = app_users.objects.get(full_name=employees)
            add_pending_task.pending_task_count = the_pending_task_count
            add_pending_task.save()

            chosen_employee = app_users.objects.get(full_name=employees)

            send_mail(
                'New Task "' + task_name + '"',
                'Good Day! A new task was assigned to you by ' + full_name + " with a task name " +
                task_name +
                ". Visit your pending task on (Future Link Here)",
                'rsb.taskmanagement@gmail.com',
                [chosen_employee.email],)

            messages.success(
                request, 'New task is added to ' + employees + ".")

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
                messages.success(
                    request, 'New category was added succesfully.')
                return redirect("category")

            else:
                dcat = request.POST.get('dcat')

                selected_category = categories.objects.get(category=dcat)
                selected_category.delete()
                messages.error(request, 'Category was deleted succesfully.')
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
                messages.success(
                    request, 'New subcategory was added succesfully.')
                return redirect("subcategory")

            else:
                cat_del = request.POST.get('cat_del')
                dsubcat = request.POST.get('dsubcat')

                selected_subcategory = subcategories.objects.get(
                    category=cat_del, subcategory=dsubcat)
                selected_subcategory.delete()
                messages.error(request, 'Subcategory was deleted succesfully.')
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
                    messages.success(
                        request, 'New details was added succesfully.')
                    return redirect("steps")

            elif 'form2' in request.POST:
                detail_to_del = request.POST.get('sub_to_del')

                selected_detail = detail.objects.get(
                    subcategory=detail_to_del)
                selected_detail.delete()
                messages.error(request, 'Details was deleted succesfully.')
                return redirect('steps')

            elif 'form3' in request.POST:
                detail_to_up = request.POST.get('sub_to_up')
                new_details = request.POST.get('new_details')

                selected_detail = detail.objects.get(
                    subcategory=detail_to_up)
                selected_detail.details = new_details
                selected_detail.save()
                messages.success(request, 'Details was updated succesfully.')
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
    print("nangyare?1")
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    username = request.user.username

    print("nangyare?2")

    today = date.today()
    date_today = today.strftime("%Y-%m-%d")
    the_user = app_users.objects.get(username=username)

    print("nangyare?3")

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print("nangyare?4")

    the_log = logbook.objects.filter(
        name=the_user.full_name, date_logged=date_today, time_logged_out="NTO").count()
    print("nangyare?5")

    if the_log == 1:
        print("nangyare?6")

        log_time_out = logbook.objects.get(
            name=the_user.full_name, date_logged=date_today, time_logged_out="NTO")
        log_time_out.time_logged_out = current_time

        time_str1 = str(log_time_out.time_logged)
        time_str2 = str(current_time)

        # convert string to time object
        time1 = datetime.strptime(time_str1, '%H:%M').time()
        time2 = datetime.strptime(time_str2, '%H:%M').time()

        # calculate the difference in minutes
        timedelta = datetime.combine(datetime.today(
        ), time2) - datetime.combine(datetime.today(), time1)
        minutes_diff = (timedelta.seconds // 60) / 60
        total = '{:0.2f}'.format(minutes_diff)

        log_time_out.total_hours = str(total)
        log_time_out.save()

        print("nangyare?7")
        logout(request)
        return redirect('index')

    else:
        print("nangyare?8")
        logout(request)
        return redirect('index')
