from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserMain, UserDoctor, Document
from doctors.models import Review


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=250, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2', 'email')


class UserMainForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        min_length=3,
        required=True,
        label='E-mail',
    )
    fio = forms.CharField(
        max_length=100,
        min_length=3,
        required=True,
        label='ФИО',
    )
    dob = forms.CharField(
        max_length=10,
        required=True,
        label='Дата рождения',
    )
    city = forms.CharField(
        min_length=3,
        max_length=200,
        required=True,
        label='Город',
    )
    timezone = forms.CharField(
        max_length=200,
        required=True,
        label='Временная зона',
    )
    gender = forms.CharField(
        max_length=6,
        required=True,
        label='Пол',
    )
    skype = forms.CharField(
        min_length=5,
        max_length=50,
        required=False,
        label='Skype',
    )
    whatsapp = forms.CharField(
        min_length=5,
        max_length=20,
        required=False,
        label='WhatsApp',
    )

    class Meta:
        model = UserMain
        fields = ['email', 'fio', 'dob', 'city', 'time_zone', 'gender', 'skype', 'whatsapp']


class UserDoctorForm(forms.ModelForm):
    specialty = forms.CharField(
        min_length=3,
        max_length=100,
        required=False,
        label='Специализация',
    )
    experience_text = forms.CharField(
        min_length=3,
        max_length=3000,
        required=False,
        label='Опыт работы',
    )
    experience_years = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        label='Стаж'
    )

    class Meta:
        model = UserDoctor
        fields = ['specialty', 'experience_text', 'experience_years']


class DocumentForm(forms.ModelForm):
    doc_name = forms.CharField(
        max_length=100,
        min_length=3,
        required=True,
        label='Название',
    )

    doc_file = forms.ImageField(required=True, label='Изображение')

    class Meta:
        model = Document
        fields = ['doc_name', 'doc_file']


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        min_length=3,
        max_length=100,
        required=False,
        label='Заголовок',
    )

    star_prof = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        label='Профессионализм'
    )

    star_pers = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        label='Личные качества'
    )

    text = forms.CharField(
        min_length=3,
        max_length=3000,
        required=True,
        label='Текст Отзыва',
    )

    class Meta:
        model = Review
        fields = ['title', 'text', 'star_prof', 'star_pers']