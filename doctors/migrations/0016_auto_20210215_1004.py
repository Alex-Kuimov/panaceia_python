# Generated by Django 3.1.4 on 2021-02-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0015_review_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='review_notify',
            field=models.BooleanField(blank=True, default=0, verbose_name='Оставить отзыв'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(blank=True, max_length=3000, verbose_name='Текст Отзыва'),
        ),
    ]
