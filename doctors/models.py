from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    data = models.DateField(blank=True, max_length=100, verbose_name='Дата')
    time = models.TimeField(max_length=100, verbose_name='Время', default='00:00:00')
    doctor_id = models.IntegerField(blank=True, verbose_name='Доктор', default=1)
    user_id = models.IntegerField(blank=True, verbose_name='Пациент', default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'