# Generated by Django 3.1.4 on 2021-01-14 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_calendar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendar',
            old_name='data',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='meeting',
            old_name='data',
            new_name='date',
        ),
    ]
