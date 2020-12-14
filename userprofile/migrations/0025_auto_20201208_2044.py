# Generated by Django 3.1.3 on 2020-12-08 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0024_auto_20201208_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdoctor',
            name='author',
            field=models.BooleanField(blank=True, null=True, verbose_name='Я автор видеолекций'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='consultant',
            field=models.BooleanField(blank=True, null=True, verbose_name='Я консультант'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='doctor',
            field=models.BooleanField(blank=True, null=True, verbose_name='Я врач'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='fullDoctor',
            field=models.BooleanField(blank=True, null=True, verbose_name='Я врач и консультант'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='orgtype',
            field=models.CharField(blank=True, choices=[('ur', 'Юридическое лицо'), ('fiz', 'Физическое лицо')], max_length=11, null=True, verbose_name='Тип организации'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='patientChildren',
            field=models.BooleanField(blank=True, null=True, verbose_name='Дети'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='patientGrown',
            field=models.BooleanField(blank=True, null=True, verbose_name='Взрослые'),
        ),
        migrations.AlterField(
            model_name='userdoctor',
            name='specialty',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Специализация'),
        ),
    ]