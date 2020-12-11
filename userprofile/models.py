from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

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

    def save_chk(self, name, request):

        if name in request.POST:
            if name == 'doctor':
                self.doctor = request.POST[name]

            if name == 'consultant':
                self.consultant = request.POST[name]

            if name == 'fullDoctor':
                self.fullDoctor = request.POST[name]

            if name == 'author':
                self.author = request.POST[name]

            if name == 'patientGrown':
                self.patientGrown = request.POST[name]

            if name == 'patientChildren':
                self.patientChildren = request.POST[name]
        else:
            if name == 'doctor':
                self.doctor = False

            if name == 'consultant':
                self.consultant = False

            if name == 'fullDoctor':
                self.fullDoctor = False

            if name == 'author':
                self.author = False

            if name == 'patientGrown':
                self.patientGrown = False

            if name == 'patientChildren':
                self.patientChildren = False

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

    # add
    def add(self, request):
        spec_post_list = []
        for item in request.POST:
            if item.find('spec[') != -1:
                spec_post_list.append(item)

        spec_model_list = []
        for spec in self:
            name = 'spec[{}]'.format(spec.id)
            spec_model_list.append(name)

        for item in spec_post_list:
            if not item in spec_model_list:
                if (request.POST[item] != ''):
                    new_spec = Specialty.objects.create(title=request.POST[item], content_id=request.user.id)
                    self.user = new_spec

    # update
    def update(self, request):
        for item in request.POST:
            if item.find('spec[') != -1:

                for spec in self:
                    name = 'spec[{}]'.format(spec.id)

                    if item == name:
                        spec.title = request.POST[name]
                        spec.save()

    # remove
    def remove(self, request):
        spec_post_list = []
        for item in request.POST:
            if item.find('spec[') != -1:
                spec_post_list.append(item)

        spec_model_list = []
        for spec in self:
            name = 'spec[{}]'.format(spec.id)
            spec_model_list.append(name)

        for item in spec_model_list:
            if not item in spec_post_list:
                item_id = re.sub(r'[^0-9.]+', r'', item)
                instance = Specialty.objects.get(id=item_id)
                instance.delete()

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserMain.objects.create(user=instance)
        UserDoctor.objects.create(user=instance)
