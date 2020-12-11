from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserMain, UserDoctor, User,Specialty
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.models import Group, User
from django.core.files.storage import FileSystemStorage
import re

def home(request):
    return render(request, 'home.html')


def user_main(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'base_generic.html', {'user_profile': user_profile})


def profile_page_view(request):
    if request.user.is_authenticated:
        user_profile = UserMain.objects.get(user=request.user)
        user_doctor = UserDoctor.objects.get(user=request.user)
        user_spec = Specialty.objects.filter(content=request.user)

        if request.path == '/profile/info/':
            return render(request, 'profile/profile.html', {'user_profile': user_profile})

        if request.path == '/profile/main/':
            return render(request, 'profile/profile_main.html', {'user_profile': user_profile, 'user_doctor': user_doctor, 'user_spec': user_spec})

        if request.path == '/profile/recomend/':
            return render(request, 'profile/recomend.html', {'user_profile': user_profile})

        if request.path == '/profile/grafik/':
            return render(request, 'profile/grafik.html', {'user_profile': user_profile})

        if request.path == '/profile/consalt/':
            return render(request, 'profile/consalt.html', {'user_profile': user_profile})

        if request.path == '/profile/videos/':
            return render(request, 'profile/videos.html', {'user_profile': user_profile})

        if request.path == '/profile/settings/':
            return render(request, 'profile/settings.html', {'user_profile': user_profile})

    else:
        return redirect('login')


def save_main_data(request):
    user_profile = UserMain.objects.get(user=request.user)
    user = User.objects.get(pk=request.user.id)

    user.email = request.POST['email']
    user.save()

    user_profile.fio = request.POST['fio']
    user_profile.dob = request.POST['dob']
    user_profile.city = request.POST['city']
    user_profile.gender = request.POST['gender']
    user_profile.time_zone = request.POST['timezone']
    user_profile.whatsapp = request.POST['whatsapp']
    user_profile.skype = request.POST['skype']

    if 'avatar' in request.FILES:
        user_profile.avatar = request.FILES['avatar']

    if request.POST['avatar_none'] == 'y':
        user_profile.avatar = ''

    user_profile.save()

    return HttpResponseRedirect(reverse('user_profile_main'))


def save_doctor_data(request):
    user_doctor = UserDoctor.objects.get(user=request.user)
    user_spec = Specialty.objects.filter(content=request.user)

    user_doctor.specialty = request.POST['specialty']
    user_doctor.orgtype = request.POST['orgtype']
    UserDoctor.save_chk(user_doctor, 'doctor', request)
    UserDoctor.save_chk(user_doctor, 'consultant', request)
    UserDoctor.save_chk(user_doctor, 'fullDoctor', request)
    UserDoctor.save_chk(user_doctor, 'author', request)

    UserDoctor.save_chk(user_doctor, 'patientGrown', request)
    UserDoctor.save_chk(user_doctor, 'patientChildren', request)

    Specialty.add(user_spec, request)
    Specialty.update(user_spec, request)
    Specialty.remove(user_spec, request)

    user_doctor.save()

    return HttpResponseRedirect(reverse('user_profile_main'))


def signup_user_view(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            signup_user.active = True
            user_group = Group.objects.get(name='users')
            user_group.user_set.add(signup_user)

            user_profile = UserMain.objects.get(user=signup_user)
            user_profile.fio = request.POST['first_name']
            user_profile.save()

            return render(request, 'profile/login.html', {'msg': 'Вы успешно зарегестрированы!'})
        else:
            return render(request, 'profile/registration_user_form.html', {'form': form})

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, 'profile/registration_user_form.html')


def signup_doctor_view(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            signup_user.active = True
            user_group = Group.objects.get(name='doctors')
            user_group.user_set.add(signup_user)

            user_profile = UserMain.objects.get(user=signup_user)
            user_profile.fio = request.POST['first_name']
            user_profile.save()

            return render(request, 'profile/login.html', {'msg': 'Вы успешно зарегестрированы!'})
        else:
            return render(request, 'profile/registration_doctor_form.html', {'form': form})

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, 'profile/registration_doctor_form.html')


def login_view(request):
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
            else:
                return redirect('registration')
        else:
            return render(request, 'profile/login.html', {'form': form})

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, 'profile/login.html',)


def logout_view(request):
    logout(request)
    return redirect('login')