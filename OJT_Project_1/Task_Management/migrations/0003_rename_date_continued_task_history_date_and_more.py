# Generated by Django 4.0.1 on 2023-03-31 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Task_Management', '0002_remove_logbook_date_logged_out'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task_history',
            old_name='date_continued',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='task_history',
            name='date_paused',
        ),
    ]
