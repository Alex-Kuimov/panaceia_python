from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimeZone(models.Model):
    name = models.CharField(blank=True, max_length=30, verbose_name='Название')
    title = models.TextField(blank=True, max_length=1000, verbose_name='Города')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Временные зоны'
        verbose_name_plural = 'Временные зоны'


class UserMain(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender_list = (
        ('male', 'Мужской'),
        ('female', 'Женский')
    )

    queryset = TimeZone.objects.all()
    time_zone_list = []
    for i in queryset:
         time_zone_list.append((i.name, i.title))

    gender = models.CharField(blank=True,  max_length=6, choices=gender_list, verbose_name='Пол')
    avatar = models.ImageField(blank=True, upload_to='images/users', verbose_name='Изображение')

    fio = models.CharField(blank=True, max_length=100, verbose_name='ФИО')
    dob = models.CharField(blank=True, max_length=10, verbose_name='Дата рождения')
    city = models.CharField(blank=True, max_length=200, verbose_name='Город')
    time_zone = models.CharField(blank=True, max_length=200, choices=time_zone_list, verbose_name='Временная зона')
    skype = models.CharField(blank=True, max_length=50, verbose_name='Skype')
    whatsapp = models.CharField(blank=True, max_length=20, verbose_name='WhatsApp')
    phone = models.CharField(blank=True, max_length=20, verbose_name='Номер телефона')
    coords = models.CharField(blank=True, max_length=200, verbose_name='Координаты')

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class UserDoctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    org_types_list = [
        ('ur', 'Юридическое лицо'),
        ('fiz', 'Физическое лицо')
    ]

    orgtype = models.CharField(blank=True, null=True, max_length=11, choices=org_types_list, verbose_name='Тип организации')

    meet_online = models.BooleanField(blank=True, null=True, verbose_name='Прием онлайн')
    meet_offline = models.BooleanField(blank=True, null=True, verbose_name='Прием оффлайн')
    patient_grown = models.BooleanField(blank=True, null=True, verbose_name='Взрослые')
    patient_children = models.BooleanField(blank=True, null=True, verbose_name='Дети')
    verified = models.BooleanField(blank=True, null=True, verbose_name='Аккаунт верифицирован')

    experience_text = models.TextField(blank=True, max_length=3000, verbose_name='Опыт работы')
    experience_years = models.CharField(blank=True, max_length=2, verbose_name='Стаж')

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Document(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(blank=True, upload_to='media/', verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Specialty(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Associations(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Членство в ассоциациях'
        verbose_name_plural = 'Членство в ассоциациях'


class Education(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    years = models.CharField(max_length=20, verbose_name='Года')
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'


class Qualification(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    years = models.CharField(max_length=20, verbose_name='Года')
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Повышение квалификации'
        verbose_name_plural = 'Повышение квалификации'


class Service(models.Model):
    content = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название')
    time = models.CharField(max_length=20, verbose_name='Время')
    price = models.CharField(max_length=20, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Support(models.Model):
    user_id = models.IntegerField(blank=True)
    user_name = models.CharField(blank=True, max_length=100)
    text = models.TextField(blank=True, max_length=3000)

    def __str__(self):
        return f'Обращение №{self.id}'

    class Meta:
        verbose_name = 'Сообщение в службу поддержки'
        verbose_name_plural = 'Сообщения в службу поддержки'


class SpecialtyList(models.Model):
    name = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(blank=True, max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список специальностей'
        verbose_name_plural = 'Список специальностей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserMain.objects.create(user=instance)
        UserDoctor.objects.create(user=instance)
