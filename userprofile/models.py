from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserMain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    USERTYPES = [('doctor', 'Доктор'),
               ('patient', 'Пациент')]

    GENDER = [('male', 'Мужской'),
               ('female', 'Женский')]

    gender = models.CharField(default=False, max_length=11, choices=GENDER, verbose_name='Пол')
    usertype = models.CharField(default=False, max_length=11, choices=USERTYPES, verbose_name='Тип')
    avatar = models.ImageField(blank=False, upload_to='images/users', verbose_name='Изображение')

    fio = models.CharField(default=False, max_length=100, verbose_name='ФИО')
    city = models.CharField(default=False, max_length=100, verbose_name='Город')
    whatsapp = models.CharField(default=False, max_length=100, verbose_name='WhatsApp')
    skype = models.CharField(default=False, max_length=100, verbose_name='Skype')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class UserDoctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ORGTYPES = [('ur', 'Юридическое лицо'),
               ('fiz', 'Физическое лицо')]

    doctor = models.BooleanField(default=False, verbose_name='Я врач')
    consultant = models.BooleanField(default=False, verbose_name='Я консультант')
    fullDoctor = models.BooleanField(default=False, verbose_name='Я врач и консультант')
    author = models.BooleanField(default=False, verbose_name='Я автор видеолекций')
    orgtype = models.CharField(default=False, max_length=11, choices=ORGTYPES, verbose_name='Тип организации')
    specialty = models.CharField(default=False, max_length=100, verbose_name='Специализация')
    patientGrown = models.BooleanField(default=False, verbose_name='Взрослые')
    patientChildren = models.BooleanField(default=False, verbose_name='Дети')

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
