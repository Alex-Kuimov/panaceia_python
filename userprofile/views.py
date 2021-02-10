from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserMain, UserDoctor, User, Specialty, Associations, Education, Qualification, Support, TimeZone, SpecialtyList, Service, Document
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, UserMainForm, UserDoctorForm, DocumentForm
from django.contrib.auth.models import Group, User
from blog.models import Article
from doctors.models import Meeting
from .utility import OneInputField, TwoInputField, ThreeInputField, CheckboxField, get_task, get_meetings_list, get_contact_list
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings


def home(request):
    specialty_list = SpecialtyList.objects.all()

    data = {
        'specialty_list': specialty_list
    }

    return render(request, 'home.html', data)


def user_main(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'base_generic.html', {'user_profile': user_profile})


@login_required
def profile_page_view(request):

    # only authenticated users
    if request.user.is_authenticated:

        # getting params
        user_profile = UserMain.objects.get(user=request.user)
        user_doctor = UserDoctor.objects.get(user=request.user)
        user_spec = Specialty.objects.filter(content=request.user)
        user_associations = Associations.objects.filter(content=request.user)
        user_education = Education.objects.filter(content=request.user)
        user_qualification = Qualification.objects.filter(content=request.user)
        user_services = Service.objects.filter(content=request.user)
        user_documents = Document.objects.filter(content=request.user)
        timezone = TimeZone.objects.all()
        articles = Article.objects.all()
        specialty_list = SpecialtyList.objects.all()

        # create data
        data = {'user_profile': user_profile}

        # pages
        if request.path == '/profile/consalt_user/':
            meetings = get_meetings_list(Meeting, Specialty, UserMain, request.user.id)
            data.update({'meetings': meetings})

        if request.path == '/profile/grafik/':
            if request.user.groups.filter(name='doctors').exists():
                return render(request, 'profile/grafik.html', data)
            else:
                return render(request, 'errs/404.html')

        if request.path == '/profile/contact_user/':
            if request.user.groups.filter(name='doctors').exists():

                contact_list = get_contact_list(Meeting, UserMain, User, request.user.id)

                data.update({'contact_list': contact_list})

                return render(request, 'profile/contact_user.html', data)
            else:
                return render(request, 'errs/404.html')

        if request.path == '/profile/info/':
            return render(request, 'profile/profile.html', data)

        if request.path == '/profile/main/':
            doctor_data = {
                'user_doctor': user_doctor,
                'user_spec': user_spec,
                'user_associations': user_associations,
                'user_education': user_education,
                'user_qualification': user_qualification,
                'user_services': user_services,
                'user_documents': user_documents,
                'specialty_list': specialty_list,
                'timezone': timezone,
            }

            data.update(doctor_data)

            return render(request, 'profile/profile_main.html', data)

        if request.path == '/profile/recomend/':
            return render(request, 'profile/recomend.html', data)

        if request.path == '/profile/consalt_user/':
            return render(request, 'profile/consalt_user.html', data)

        if request.path == '/profile/videos/':
            return render(request, 'profile/videos.html', data)

        if request.path == '/profile/settings/':
            return render(request, 'profile/settings.html', data)

        if request.path == '/profile/articles/':
            data.update({'articles': articles})
            return render(request, 'profile/articles.html', data)

        if request.path == '/profile/reviews/':
            if request.user.groups.filter(name='users').exists():
                doctor_id = request.GET['doctor_id']
                data.update({'doctor_id': doctor_id})
                return render(request, 'profile/reviews.html', data)
            else:
                return render(request, 'errs/404.html')

    else:
        return redirect('login')


@login_required
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
            user_profile.coords = request.POST['coords']
            user_profile.gender = request.POST['gender']
            user_profile.time_zone = request.POST['timezone']
            user_profile.whatsapp = request.POST['whatsapp']
            user_profile.skype = request.POST['skype']
            user_profile.phone = request.POST['phone']

            if 'avatar' in request.FILES:
                user_profile.avatar = request.FILES['avatar']

            if request.POST['avatar_none'] == 'y':
                user_profile.avatar = ''

            user_profile.save()

    return HttpResponseRedirect(reverse('save_data_success'))


@login_required
def save_doctor_data(request):
    if request.method == 'POST':
        form = UserDoctorForm(request.POST)

        if form.is_valid():

            # get data
            user_doctor = UserDoctor.objects.get(user=request.user)
            user_spec = Specialty.objects.filter(content=request.user)
            user_associations = Associations.objects.filter(content=request.user)
            user_education = Education.objects.filter(content=request.user)
            user_qualification = Qualification.objects.filter(content=request.user)
            user_service = Service.objects.filter(content=request.user)

            # simple data save
            user_doctor.orgtype = request.POST['orgtype']
            user_doctor.experience_text = request.POST['experience_text']
            user_doctor.experience_years = request.POST['experience_years']

            # checkbox data save
            CheckboxField.save(user_doctor, 'meet_online', request)
            CheckboxField.save(user_doctor, 'meet_offline', request)
            CheckboxField.save(user_doctor, 'patient_grown', request)
            CheckboxField.save(user_doctor, 'patient_children', request)

            user_doctor.save()

            # multi input field data save
            OneInputField.add(Specialty, user_spec, request, 'spec')
            OneInputField.update(Specialty, user_spec, request, 'spec')
            OneInputField.remove(Specialty, user_spec, request, 'spec')

            OneInputField.add(Associations, user_associations, request, 'as')
            OneInputField.update(Associations, user_associations, request, 'as')
            OneInputField.remove(Associations, user_associations, request, 'as')

            TwoInputField.add(Education, user_education, request, 'ed', 'edy')
            TwoInputField.update(Education, user_education, request, {'ed': 'name', 'edy': 'years'})
            TwoInputField.remove(Education, user_education, request, 'ed')

            TwoInputField.add(Qualification, user_qualification, request, 'qu', 'quy')
            TwoInputField.update(Qualification, user_qualification, request, {'qu': 'name', 'quy': 'years'})
            TwoInputField.remove(Qualification, user_qualification, request, 'qu')

            ThreeInputField.add(Service, user_service, request, 'se', 'set', 'sep')
            ThreeInputField.update(Service, user_service, request, {'se': 'name', 'set': 'time', 'sep': 'price'})
            ThreeInputField.remove(Service, user_service, request, 'se')

    return HttpResponseRedirect(reverse('save_data_success'))


def signup_view(request, user_group_type, template):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            signup_user.active = True
            user_group = Group.objects.get(name=user_group_type)
            user_group.user_set.add(signup_user)

            user_profile = UserMain.objects.get(user=signup_user)
            user_profile.fio = request.POST['first_name']
            user_profile.save()

            subject = 'Регистрация на сайте Panaceia'
            content = '<p>Поздравляем! Вы успешно зарегистрированы на сайте Panaceia.</p>'
            to = [request.POST['email']]
            _from = settings.DEFAULT_FROM_EMAIL

            email = EmailMessage(
                subject,
                content,
                _from,
                to,
                headers={'Reply-To': _from}
            )

            email.content_subtype = 'html'
            email.send()

            return render(request, 'profile/login.html', {'msg': 'Вы успешно зарегестрированы!'})
        else:
            return render(request, template, {'form': form})

    if request.user.is_authenticated:
        return redirect('user_profile')
    else:
        return render(request, template)


def signup_user_view(request):
    user_group = 'users'
    template = 'profile/registration_user_form.html'

    try:
        result = signup_view(request, user_group, template)
    except:
        result = render(request, 'profile/login.html', {'msg': 'Возможно произошла ошибка!'})

    return result


def signup_doctor_view(request):
    user_group = 'doctors'
    template = 'profile/registration_doctor_form.html'

    try:
        result = signup_view(request, user_group, template)
    except:
        result = render(request, 'profile/login.html', {'msg': 'Возможно произошла ошибка!'})

    return result


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


@login_required
def change_user_pass(request):
    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            user.set_password(request.POST['password'])
            user.save()
        else:
            return render(request, 'profile/settings.html', {'msg': 'Пароли не совпадают!'})

    return redirect('user_profile_settings')


@login_required
def save_user_doc(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            if 'doc_file' in request.FILES:
                instance = Document.objects.create(title=request.POST['doc_name'], image=request.FILES['doc_file'], content_id=request.user.id)
                Document.user = instance

    return HttpResponseRedirect(reverse('save_data_success'))


@login_required
def remove_user_doc(request):
    if request.method == 'GET':
        index = request.GET['doc_id']
        instance = Document.objects.get(id=index)
        instance.delete()
    return HttpResponseRedirect(reverse('user_profile_main'))


@login_required
def save_support_message(request):
    if request.method == 'POST':
        user_id = request.user.id
        user_name = request.user.username
        message = request.POST['message']

        s = Support.objects.create(user_id=user_id, user_name=user_name, text=message)
        s.save()

    return render(request, 'profile/settings.html', {'txt': 'Сообщение отправлено!'})


@login_required
def send_file_for_verified(request):
    user_profile = UserMain.objects.get(user=request.user)
    user_name = request.user.username

    fio = user_profile.fio
    phone = user_profile.phone
    user_email = request.user.email

    user_id = request.user.id
    subject = 'Верификация пользователя - ' + user_name + '(' + str(user_id) + ')'
    content = '<p>Пользователь <b>' + user_name + '</b> запросил верификацию.</p>'

    if fio != '':
        content += '<p><b>ФИО:</b> ' + fio + '</p>'

    if user_email != '':
        content += '<p><b>E-mail:</b> ' + user_email + '</p>'

    if phone != '':
        content += '<p><b>Телефон:</b> ' + phone + '</p>'

    _from = settings.DEFAULT_FROM_EMAIL
    to = [settings.ADMIN_EMAIL]

    email = EmailMessage(
        subject,
        content,
        _from,
        to,
        headers={'Reply-To': _from}
    )

    if request.FILES:
        passport_photo = request.FILES['passport_photo']
        diplom_photo = request.FILES['diplom_photo']
        email.attach(passport_photo.name, passport_photo.read(), passport_photo.content_type)
        email.attach(diplom_photo.name, diplom_photo.read(), diplom_photo.content_type)

    email.content_subtype = 'html'
    email.send()

    return HttpResponseRedirect(reverse('save_verification_success'))


@login_required
def save_data_success(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'profile/success.html', {'user_profile': user_profile})


@login_required
def save_verification_success(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'profile/verification_success.html', {'user_profile': user_profile})


@login_required
def save_consalt_success(request):
    user_profile = UserMain.objects.get(user=request.user)
    return render(request, 'profile/success_consalt.html', {'user_profile': user_profile})


@login_required
def get_task_view(request):
    user_profile = UserMain.objects.get(user=request.user)
    user_doctor = UserDoctor.objects.get(user=request.user)

    meeting_new = get_task(UserMain, Meeting, request.user.id, 'new')
    meeting_work = get_task(UserMain, Meeting, request.user.id, 'work')
    meeting_success = get_task(UserMain, Meeting, request.user.id, 'success')
    meeting_reject = get_task(UserMain, Meeting, request.user.id, 'reject')

    data = {
        'user_profile': user_profile,
        'user_doctor': user_doctor,
        'meeting_new': meeting_new,
        'meeting_work': meeting_work,
        'meeting_success': meeting_success,
        'meeting_reject': meeting_reject,
    }

    if request.user.groups.filter(name='doctors').exists():
        return render(request, 'profile/consalt_doctor.html', data)


def error_404(request, exception):
    return render(request, 'errs/404.html')


def error_500(request):
    return render(request, 'errs/500.html')