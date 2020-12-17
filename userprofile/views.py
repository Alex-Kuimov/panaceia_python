from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserMain, UserDoctor, User, Specialty, Associations, Education, Qualification, Support, TimeZone
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, UserMainForm
from django.contrib.auth.models import Group, User
from blog.models import Article
from .utility import UserFieldUtility

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
        user_associations = Associations.objects.filter(content=request.user)
        user_education = Education.objects.filter(content=request.user)
        user_qualification = Qualification.objects.filter(content=request.user)
        timezone = TimeZone.objects.all()
        articles = Article.objects.all()

        data = {
            'user_profile': user_profile,
            'user_doctor': user_doctor,
            'user_spec': user_spec,
            'user_associations': user_associations,
            'user_education': user_education,
            'user_qualification': user_qualification,
            'timezone': timezone,
            'articles': articles
        }

        if request.path == '/profile/info/':
            return render(request, 'profile/profile.html', data)

        if request.path == '/profile/main/':
            return render(request, 'profile/profile_main.html', data)

        if request.path == '/profile/recomend/':
            return render(request, 'profile/recomend.html', data)

        if request.path == '/profile/grafik/':
            return render(request, 'profile/grafik.html', data)

        if request.path == '/profile/consalt/':
            return render(request, 'profile/consalt.html', data)

        if request.path == '/profile/videos/':
            return render(request, 'profile/videos.html', data)

        if request.path == '/profile/settings/':
            return render(request, 'profile/settings.html', data)

        if request.path == '/profile/articles/':
            return render(request, 'profile/articles.html', data)

    else:
        return redirect('login')


def save_main_data(request):
    if request.method == 'POST':
        form = UserMainForm(request.POST, request.FILES)

        if form.is_valid():
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
    user_associations = Associations.objects.filter(content=request.user)
    user_education = Education.objects.filter(content=request.user)
    user_qualification = Qualification.objects.filter(content=request.user)

    user_doctor.specialty = request.POST['specialty']
    user_doctor.orgtype = request.POST['orgtype']
    user_doctor.experienceText = request.POST['experienceText']
    user_doctor.experienceYears = request.POST['experienceYears']

    UserDoctor.save_chk(user_doctor, 'doctor', request)
    UserDoctor.save_chk(user_doctor, 'consultant', request)
    UserDoctor.save_chk(user_doctor, 'fullDoctor', request)
    UserDoctor.save_chk(user_doctor, 'author', request)

    UserDoctor.save_chk(user_doctor, 'patientGrown', request)
    UserDoctor.save_chk(user_doctor, 'patientChildren', request)

    Specialty.add(user_spec, request)
    Specialty.update(user_spec, request)
    Specialty.remove(user_spec, request)

    Associations.add(user_associations, request)
    Associations.update(user_associations, request)
    Associations.remove(user_associations, request)

    Education.add(user_education, request)
    Education.update(user_education, request)
    Education.remove(user_education, request)

    UserFieldUtility.add(user_qualification, Qualification, request, 'qu', 'quy')
    UserFieldUtility.update(user_qualification, request, {'qu': 'name', 'quy': 'years'})
    UserFieldUtility.remove(user_qualification, Qualification, request, 'qu')

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


def change_user_pass(request):
    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            user.set_password(request.POST['password'])
            user.save()
        else:
            return render(request, 'profile/settings.html', {'msg': 'Пароли не совпадают!'})

    return redirect('user_profile_settings')


def save_user_settings(request):
    user_profile = UserMain.objects.get(user=request.user)
    user = User.objects.get(pk=request.user.id)

    user.email = request.POST['email']
    user.save()

    user_profile.phone = request.POST['phone']
    user_profile.save()

    return redirect('user_profile_settings')


def save_support_message(request):
    if request.method == 'POST':
        user_id = request.user.id
        user_name = request.user.username
        message = request.POST['message']

        s = Support.objects.create(user_id=user_id, user_name=user_name, text=message)
        s.save()

    return render(request, 'profile/settings.html', {'txt': 'Сообщение отправлено!'})