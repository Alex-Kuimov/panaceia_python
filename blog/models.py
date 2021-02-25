from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from .utility import slugify


class Article(models.Model):
    title = models.CharField(blank=True, max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(blank=True, max_length=100, unique=True)
    text = HTMLField(blank=True, max_length=10000, verbose_name='Текст')
    preview = models.TextField(blank=True, max_length=500, verbose_name='Отрывок')
    image = models.ImageField(blank=True, upload_to='images/blog', verbose_name='Изображение')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    user = models.IntegerField(blank=True, verbose_name='Автор', default=1)

    status_list = [
        ('new', 'Новая'),
        ('review', 'Рассмотрение'),
        ('success', 'Одобрено'),
        ('reject', 'Отказ'),
        ('archive', 'Архив'),
    ]

    status = models.CharField(blank=True, null=True, max_length=11, choices=status_list, verbose_name='Статус')

    def save(self, *args, **kwargs):
        object_list = Article.objects.filter(title=self.title)

        if len(object_list) == 0:
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.title) + '-' + str(len(object_list))

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
