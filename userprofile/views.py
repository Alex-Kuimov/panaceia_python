from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserMain, UserDoctor, User
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.models import Group, User


def home(request):
    return render(request, 'home.html')


def user_main(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'base_generic.html', {'user_profile': user_profile})


def profile_page_view(request):
    if request.user.is_authenticated:
        user_profile = UserMain.objects.get(user=request.user)

        if request.path == '/profile/info/':
            return render(request, 'profile/profile.html', {'user_profile': user_profile})

        if request.path == '/profile/main/':
            return render(request, 'profile/profile_main.html', {'user_profile': user_profile})

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
    user_profile.fio = request.POST['fio']
    user_profile.city = request.POST['city']
    user_profile.whatsapp = request.POST['whatsapp']
    user_profile.skype = request.POST['skype']
    user_profile.save()

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
            return render(request, 'profile/login.html')

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, 'profile/registration_user_form.html', {'form': form})


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
            return render(request, 'profile/login.html')

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, 'profile/registration_doctor_form.html', {'form': form})


def login_view(request):
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

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, 'profile/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')