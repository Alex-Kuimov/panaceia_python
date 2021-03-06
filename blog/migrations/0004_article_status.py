# Generated by Django 3.1.4 on 2021-02-18 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210216_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(blank=True, choices=[('new', 'Новая'), ('review', 'Рассмотрение'), ('success', 'Выполнено'), ('reject', 'Отказ'), ('archive', 'Архив')], max_length=11, null=True, verbose_name='Статус'),
        ),
    ]
