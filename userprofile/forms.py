from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserMain


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