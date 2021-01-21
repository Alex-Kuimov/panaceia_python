from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    date = models.DateField(blank=True, max_length=100, verbose_name='Дата')
    time_start = models.TimeField(max_length=100, verbose_name='Время начало', default='00:00:00')
    time_end = models.TimeField(max_length=100, verbose_name='Время конец', default='00:00:00')
    doctor_id = models.IntegerField(blank=True, verbose_name='Доктор', default=1)
    user_id = models.IntegerField(blank=True, verbose_name='Пациент', default=1)
    service_id = models.IntegerField(blank=True, verbose_name='Услуга', default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'


class Calendar(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    date = models.DateField(blank=True, max_length=100, verbose_name='Дата')
    time_start = models.TimeField(max_length=100, verbose_name='Время начало', default='00:00:00')
    time_end = models.TimeField(max_length=100, verbose_name='Время конец', default='00:00:00')
    doctor_id = models.IntegerField(blank=True, verbose_name='Доктор', default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'