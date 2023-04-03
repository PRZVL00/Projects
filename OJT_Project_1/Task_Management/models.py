from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class PrefixedAutoField(models.AutoField):
    description = _("Auto-incremented ID with prefix")

    def __init__(self, prefix, *args, **kwargs):
        self.prefix = prefix
        super().__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return f"{self.prefix}{value}"


class app_users(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True)
    id_number = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=11)
    position = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    active_task_count = models.CharField(max_length=11)
    pending_task_count = models.CharField(max_length=11)
    profile_pic = models.ImageField(upload_to="profile_pic/")


class tasks(models.Model):
    task_id = PrefixedAutoField("RSB-Task-", primary_key=True, unique=True)
    task_name = models.CharField(max_length=30)
    task_id = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    subcategory = models.CharField(max_length=30)
    details = models.TextField(max_length=1000)
    assigned_by = models.CharField(max_length=30)
    assigned_to = models.CharField(max_length=30)
    date_published = models.CharField(max_length=30)
    date_started = models.CharField(max_length=30)
    time_started = models.CharField(max_length=30)
    date_completed = models.CharField(max_length=30)
    time_completed = models.CharField(max_length=30)
    total_hours = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    active_status = models.CharField(max_length=30)


class task_history(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    task_id = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    time_continued = models.CharField(max_length=30)
    time_paused = models.CharField(max_length=30)
    man_hours = models.CharField(max_length=30)
    status = models.CharField(max_length=30)


class logbook(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    id_number = models.CharField(max_length=30)
    date_logged = models.CharField(max_length=30)
    time_logged = models.CharField(max_length=30)
    time_logged_out = models.CharField(max_length=30)
    total_hours = models.CharField(max_length=30)


class categories(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.CharField(max_length=30)


class subcategories(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.CharField(max_length=30)
    subcategory = models.CharField(max_length=30)


class detail(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.CharField(max_length=30)
    subcategory = models.CharField(max_length=30)
    details = models.TextField(max_length=1000)
