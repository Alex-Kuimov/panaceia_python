from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Meeting(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    date = models.DateField(blank=True, max_length=100, verbose_name='Дата')
    time_start = models.TimeField(max_length=100, verbose_name='Время начало', default='00:00:00')
    time_end = models.TimeField(max_length=100, verbose_name='Время конец', default='00:00:00')
    doctor_id = models.IntegerField(blank=True, verbose_name='Доктор', default=1)
    user_id = models.IntegerField(blank=True, verbose_name='Пациент', default=1)
    service_id = models.IntegerField(blank=True, verbose_name='Услуга', default=1)
    sort_id = models.IntegerField(blank=True, verbose_name='Индекс сортитровки', default=1)
    email_notify = models.BooleanField(blank=True, verbose_name='Уведомление на почту', default=0)
    review_notify = models.BooleanField(blank=True, verbose_name='Оставить отзыв', default=0)

    status_list = [
        ('new', 'Новая'),
        ('work', 'В работе'),
        ('success', 'Выполнено'),
        ('reject', 'Отказ'),
        ('archive', 'Архив'),
    ]

    status = models.CharField(blank=True, null=True, max_length=11, choices=status_list, verbose_name='Статус')

    def __str__(self):
        return self.title + ' - doctor_id: ' + str(self.doctor_id) + ' - user_id: ' + str(self.user_id)

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


class Review(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    text = models.TextField(blank=True, max_length=3000, verbose_name='Текст Отзыва')
    doctor_id = models.IntegerField(blank=True, verbose_name='Доктор', default=1)
    user_id = models.IntegerField(blank=True, verbose_name='Пациент', default=1)
    star_prof = models.IntegerField(blank=True, verbose_name='Профессионализм', default=0)
    star_pers = models.IntegerField(blank=True, verbose_name='Личные качества', default=0)
    date = models.DateTimeField(verbose_name='Создан', default=timezone.now)

    def __str__(self):
        return self.title + ' - doctor_id: ' + str(self.doctor_id) + ' - user_id: ' + str(self.user_id)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
