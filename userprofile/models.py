from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserMain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    test = 'test'

    GENDER = [('male', 'Мужской'),
               ('female', 'Женский')]

    TIMEZONE = [('UTC +3', '(UTC +3) Москва, Санкт-Петербург, Воронеж, Казань'),
                ('UTC +7', '(UTC +7): Республика Алтай, Алтайский край, Новосибирская, Омская, Томская области')]

    gender = models.CharField(blank=True,  max_length=11, choices=GENDER, verbose_name='Пол')
    avatar = models.ImageField(blank=True, upload_to='images/users', verbose_name='Изображение')

    fio = models.CharField(blank=True, max_length=100, verbose_name='ФИО')
    dob = models.CharField(blank=True, max_length=100, verbose_name='Дата рождения')
    city = models.CharField(blank=True, max_length=100, verbose_name='Город')
    time_zone = models.CharField(blank=True, max_length=150, choices=TIMEZONE, verbose_name='Временная зона')
    whatsapp = models.CharField(blank=True, max_length=100, verbose_name='WhatsApp')
    skype = models.CharField(blank=True, max_length=100, verbose_name='Skype')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class UserDoctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ORGTYPES = [('ur', 'Юридическое лицо'),
               ('fiz', 'Физическое лицо')]

    doctor = models.BooleanField(blank=True, null=True, verbose_name='Я врач')
    consultant = models.BooleanField(blank=True, null=True, verbose_name='Я консультант')
    fullDoctor = models.BooleanField(blank=True, null=True, verbose_name='Я врач и консультант')
    author = models.BooleanField(blank=True, null=True, verbose_name='Я автор видеолекций')
    orgtype = models.CharField(blank=True, null=True, max_length=11, choices=ORGTYPES, verbose_name='Тип организации')
    specialty = models.CharField(blank=True, max_length=100, verbose_name='Специализация')
    patientGrown = models.BooleanField(blank=True, null=True, verbose_name='Взрослые')
    patientChildren = models.BooleanField(blank=True, null=True, verbose_name='Дети')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Document(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(blank=True, upload_to='media/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Specialty(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название')

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserMain.objects.create(user=instance)
        UserDoctor.objects.create(user=instance)
