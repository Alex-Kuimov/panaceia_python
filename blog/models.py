from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    text = models.TextField(blank=True, max_length=10000, verbose_name='Текст')
    image = models.ImageField(blank=True, upload_to='images/blog', verbose_name='Изображение')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'