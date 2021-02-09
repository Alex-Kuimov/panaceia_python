import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from userprofile.models import UserMain, UserDoctor, User, Service, Specialty, SpecialtyList
from .models import Meeting, Calendar
from .utility import decl_of_num, send_notify, get_email, get_doctor_list
from django.views.decorators.csrf import requires_csrf_token
from django.urls import reverse
from django.shortcuts import get_list_or_404, get_object_or_404



def doctors_map_all_view(request):
    count = len(User.objects.filter(groups__name='doctors'))

    data = {
        'title': 'Все специалисты',
        'count': count,
        'all': 'y'
    }

    return render(request, 'doctor/doctors_map.html', data)


def doctors_map_view(request, slug):
    specialty_title = SpecialtyList.objects.filter(slug=slug).values('name')[0]['name']
    count = len(User.objects.filter(groups__name='doctors', specialty__title=specialty_title))

    data = {
        'title': specialty_title,
        'count': count,
        'slug': slug,
        'all': 'n'
    }

    return render(request, 'doctor/doctors_map.html', data)


def doctors_list_all_view(request):
    data = get_doctor_list(request, '')
    return render(request, 'doctor/doctors_list.html', data)


def doctors_list_view(request, slug):
    data = get_doctor_list(request, slug)
    return render(request, 'doctor/doctors_list.html', data)


def doctor_detail_view(request, slug):
    user_id = slug
    user = get_object_or_404(User, id=user_id)

    if user.groups.filter(name='doctors').exists():
        doctor_main = UserMain.objects.get(user=user_id)
        doctor = UserDoctor.objects.get(user=user_id)
        services = Service.objects.filter(content=user_id)
        user_spec = ', '.join([str(i) for i in Specialty.objects.filter(content=user_id).order_by('?')[:4]])

        if doctor.experience_years != '':
            words = ['год', 'года', 'лет']
            num = int(doctor.experience_years)
            years = decl_of_num(num, words)
            experience = 'Стаж: ' + str(num) + ' ' + years
        else:
            experience = ''

        if doctor_main.avatar != '':
            avatar = 'media/' + str(doctor_main.avatar)
        else:
            avatar = 'medicsite/static/img/user.png'

        count_meeting = len(Meeting.objects.filter(doctor_id=user_id))

        total_service_price = 0
        count_service_item = len(services)
        average_price = 0

        for service in services:
            total_service_price = total_service_price + int(service.price)

        if count_service_item != 0:
            average_price = round(total_service_price / count_service_item)

        patients = ''
        if doctor.patient_grown:
            patients = patients + 'взрослые, '

        if doctor.patient_children:
            patients = patients + 'дети, '

        meet = ''
        if doctor.meet_online:
            meet = meet + 'online, '

        if doctor.meet_offline:
            meet = meet + 'offline, '

        doc = {
            'id': user_id,
            'fio': doctor_main.fio,
            'city': doctor_main.city,
            'phone': doctor_main.phone,
            'avatar': avatar,
            'specialty': user_spec,
            'experience_years': experience,
            'coords': doctor_main.coords,
            'average_price': average_price,
            'count_meeting': count_meeting,
            'meet': meet[:-2],
            'patients': patients[:-2],
        }

        return render(request, 'doctor/doctor_detail.html', doc)
    else:
        return render(request, 'errs/404.html')


@requires_csrf_token
def get_doctors_list(request):

    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:
        slug = request.GET['slug']

        if slug == '':
            users = User.objects.filter(groups__name='doctors')
        else:
            specialty_title = SpecialtyList.objects.filter(slug=slug).values('name')[0]['name']
            users = User.objects.filter(groups__name='doctors', specialty__title=specialty_title)

        doctors = list()

        for user in users:
            doctor_main = UserMain.objects.get(user=user)
            doctor = UserDoctor.objects.get(user=user)
            services = Service.objects.filter(content=user.id)
            user_spec = ', '.join([str(i) for i in Specialty.objects.filter(content=user.id).order_by('?')[:4]])

            if doctor.experience_years != '':
                words = ['год', 'года', 'лет']
                num = int(doctor.experience_years)
                years = decl_of_num(num, words)
                experience = 'Стаж: ' + str(num) + ' ' + years
            else:
                experience = ''

            if doctor_main.avatar != '':
                avatar = 'media/' + str(doctor_main.avatar)
            else:
                avatar = 'medicsite/static/img/user.png'

            count_meeting = len(Meeting.objects.filter(doctor_id=user.id))

            total_service_price = 0
            count_service_item = len(services)
            average_price = 0

            for service in services:
                total_service_price = total_service_price + int(service.price)

            if count_service_item != 0:
                average_price = round(total_service_price / count_service_item)

            patients = ''
            if doctor.patient_grown:
                patients = patients + 'взрослые, '

            if doctor.patient_children:
                patients = patients + 'дети, '

            meet = ''
            if doctor.meet_online:
                meet = meet + 'online, '

            if doctor.meet_offline:
                meet = meet + 'offline, '

            button = ''
            if request.user.is_authenticated:
                if request.user.groups.filter(name='users').exists():
                    if count_service_item != 0:
                        button = '<div class="appointment appointment-btn set-doctor-id show-modal" doctor-id="' + str(user.id) + '">Записаться на прием</div>'
            else:
                button = '<p>Чтобы записаться на прием, нужно авторизоваться сайте.</p>'

            _doctor = {
                'id': user.id,
                'fio': doctor_main.fio,
                'city': doctor_main.city,
                'phone': doctor_main.phone,
                'avatar': avatar,
                'specialty': user_spec,
                'experience_years': experience,
                'coords': doctor_main.coords,
                'average_price': average_price,
                'count_meeting': count_meeting,
                'meet': meet[:-2],
                'patients': patients[:-2],
                'button': button,
            }

            doctors.append(_doctor)

    else:
        doctors = 'csrf err'

    return HttpResponse(
        json.dumps(doctors),
        content_type="application/json"
    )


@requires_csrf_token
def get_calendar(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:

            if request.method == 'GET' and 'doctor_id' in request.GET:
                doctor_id = request.GET['doctor_id']
            else:
                doctor_id = request.user.id

            calendar_object_list = Calendar.objects.filter(doctor_id=doctor_id)
            user_services = Service.objects.filter(content=doctor_id)

            calendar = list()
            services = list()

            for service in user_services:

                _services = {
                    'id': service.id,
                    'name': service.name,
                    'time': service.time,
                }

                services.append(_services)

            for calendar_item in calendar_object_list:
                _calendar = {
                    'id': calendar_item.id,
                    'title': calendar_item.title,
                    'date': str(calendar_item.date),
                    'time_start': str(calendar_item.time_start),
                    'time_end': str(calendar_item.time_end),
                    'services': services,
                }

                calendar.append(_calendar)

            result = calendar

        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def create_event(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:
            title = 'График'

            date = request.GET['date']
            date_format = "%d.%m.%Y"
            date = datetime.strptime(date, date_format)
            date = date.strftime("%Y-%m-%d")

            time_start = request.GET['time_start']
            time_end = request.GET['time_end']

            doctor_id = request.user.id

            event = Calendar.objects.create(title=title, date=date, time_start=time_start, time_end=time_end, doctor_id=doctor_id)

            try:
                event.save()
                result = event.id
            except:
                result = 'save err'

        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def update_event(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:
            event_id = request.GET['event_id']
            date = request.GET['date']
            date_format = "%d.%m.%Y"
            date = datetime.strptime(date, date_format)
            date = date.strftime("%Y-%m-%d")

            time_start = request.GET['time_start']
            time_end = request.GET['time_end']

            event = Calendar.objects.filter(pk=event_id)
            event.update(date=date, time_start=time_start, time_end=time_end)
            result = 'ok'
        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def delete_event(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:
            event_id = request.GET['event_id']

            instance = Calendar.objects.get(id=event_id)
            instance.delete()
            result = 'ok'
        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def create_meeting(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:

            date = request.GET['app-date']
            time_start = request.GET['app-time-start']
            time_end = request.GET['app-time-end']
            doctor_id = request.GET['app-doctor-id']
            user_id = request.GET['app-user-id']
            service_id = request.GET['app-service']
            title = 'Консультация'

            if date != '' and time_start != '' and time_end != '' and doctor_id != '' and user_id != '' and service_id != '':
                date_to_send = date
                date_format = "%d.%m.%Y"
                date = datetime.strptime(date, date_format)
                date = date.strftime("%Y-%m-%d")

                meeting = Meeting.objects.create(
                    title=title,
                    date=date,
                    time_start=time_start,
                    time_end=time_end,
                    doctor_id=doctor_id,
                    user_id=user_id,
                    service_id=service_id,
                    sort_id=1,
                    status='new',
                )

            try:
                meeting.save()

                subject = 'Запись на консультацию'
                text = '<p>К Вам записались на консультацию. ' + date_to_send + ' в ' + time_start
                to = get_email(doctor_id)
                send_notify(to, text, subject)

                text = '<p>Вы записались на консультацию. ' + date_to_send + ' в ' + time_start
                to = get_email(user_id)
                send_notify(to, text, subject)

                result = 'ok'
            except:
                result = 'save err'
        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def get_meetings(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:
            doctor_id = request.GET['doctor_id']
            date = request.GET['date']

            date_format = "%d.%m.%Y"
            date = datetime.strptime(date, date_format)
            date = date.strftime("%Y-%m-%d")

            meetings = list()
            meeting_object_list = Meeting.objects.filter(doctor_id=doctor_id, date=date, status='new') | Meeting.objects.filter(doctor_id=doctor_id, date=date, status='work')

            for meeting in meeting_object_list:

                _meeting = {
                    'id': meeting.id,
                    'time_start': str(meeting.time_start),
                    'time_end': str(meeting.time_end),
                }

                meetings.append(_meeting)

            result = meetings

        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def get_meeting(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:

        if request.user.is_authenticated:
            meeting_id = request.GET['meeting_id']

            meetings = list()
            meeting_object_list = Meeting.objects.filter(pk=meeting_id)

            for meeting in meeting_object_list:
                user_services = Service.objects.filter(id=meeting.service_id)
                services = list()

                for service in user_services:
                    _services = {
                        'id': service.id,
                        'name': service.name,
                        'time': service.time,
                    }

                    services.append(_services)

                _meeting = {
                    'id': meeting.id,
                    'date': str(meeting.date),
                    'time_start': str(meeting.time_start),
                    'user': UserMain.objects.filter(user=meeting.user_id).values('fio')[0],
                    'phone': UserMain.objects.filter(user=meeting.user_id).values('phone')[0]['phone'],
                    'whatsapp': UserMain.objects.filter(user=meeting.user_id).values('whatsapp')[0]['whatsapp'],
                    'skype': UserMain.objects.filter(user=meeting.user_id).values('skype')[0]['skype'],
                    'email': User.objects.get(pk=meeting.user_id).email,
                    'services': services,
                }

                meetings.append(_meeting)

            result = meetings

        else:
            result = 'auth err'

    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def update_meeting(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:
        if request.user.is_authenticated:
            items = request.GET['items']
            meetings = json.loads(items)

            for key in meetings:
                id = meetings[key]['id']
                status = meetings[key]['status']
                sort = meetings[key]['sort']

                meeting = Meeting.objects.filter(pk=id)
                meeting.update(status=status, sort_id=sort)
                user_id = meeting.values('user_id')[0]['user_id']
                email_notify = meeting.values('email_notify')[0]['email_notify']

                if status == 'work' and email_notify != 1:
                    subject = 'Запись на консультацию успешно подтверждена'
                    text = '<p>Запись на консультацию #' + id + ' успешно подтверждена.</p>'
                    to = get_email(user_id)
                    send_notify(to, text, subject)
                    meeting.update(email_notify=1)

            result = 'ok'
        else:
            result = 'auth err'
    else:
        result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


@requires_csrf_token
def archive_meeting(request):
    csrf_token = request.headers.get("api-csrftoken")
    csrf_cookie = request.META.get("CSRF_COOKIE")

    if csrf_token == csrf_cookie:
        if request.user.is_authenticated:
            meeting_id = request.GET['meeting_id']
            meeting = Meeting.objects.filter(pk=meeting_id)
            meeting.update(status='archive')
            result = 'ok'
        else:
            result = 'auth err'
    else:
       result = 'csrf err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


def reject_meeting(request):
    if request.user.is_authenticated:
        meeting_id = request.GET['meeting_id']
        meeting = Meeting.objects.filter(pk=meeting_id)
        meeting.update(status='reject')
        doctor_id = meeting.values('doctor_id')[0]['doctor_id']

        subject = 'Отказ от консультации'
        text = 'От консультации #'+meeting_id+' отказались.'
        to = get_email(doctor_id)

        send_notify(to, text, subject)

    return HttpResponseRedirect(reverse('save_consalt_success'))