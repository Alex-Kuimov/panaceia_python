# Generated by Django 3.1.3 on 2020-12-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0020_usermain_time_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermain',
            name='time_zone',
            field=models.CharField(blank=True, choices=[('(UTC +3) Москва, Санкт-Петербург, Воронеж, Казань', '(UTC +3) Москва, Санкт-Петербург, Воронеж, Казань'), ('(UTC +7): Республика Алтай, Алтайский край, Новосибирская, Омская, Томская области', '(UTC +7): Республика Алтай, Алтайский край, Новосибирская, Омская, Томская области')], max_length=150, verbose_name='Временная зона'),
        ),
    ]