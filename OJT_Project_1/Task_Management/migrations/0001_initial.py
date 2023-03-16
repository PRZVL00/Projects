# Generated by Django 4.0.1 on 2023-03-16 00:38

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='detail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category', models.CharField(max_length=30)),
                ('subcategory', models.CharField(max_length=30)),
                ('details', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='logbook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('id_number', models.CharField(max_length=30)),
                ('date_logged', models.CharField(max_length=30)),
                ('time_logged', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='subcategories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category', models.CharField(max_length=30)),
                ('subcategory', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('task_name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('subcategory', models.CharField(max_length=30)),
                ('details', models.TextField(max_length=1000)),
                ('assigned_by', models.CharField(max_length=30)),
                ('assigned_to', models.CharField(max_length=30)),
                ('date_published', models.CharField(max_length=30)),
                ('date_completed', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('active_status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='app_users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('id_number', models.CharField(max_length=30)),
                ('contact_number', models.CharField(max_length=11)),
                ('position', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(upload_to='profile_pic/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
