# Generated by Django 3.1.4 on 2021-02-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='preview',
            field=models.TextField(blank=True, max_length=500, verbose_name='Отрывок'),
        ),
    ]
