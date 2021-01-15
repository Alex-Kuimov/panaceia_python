import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from userprofile.models import UserMain, UserDoctor, User
from .models import Meeting, Calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utility import decl_of_num


def doctors_map_view(request):
    data = {}
    return render(request, 'doctors_map.html', data)


def doctors_list_view(request):
    object_list = User.objects.filter(groups__name='doctors')
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    doctors = list()

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    for user in users:
        doctor_main = UserMain.objects.get(user=user)
        doctor = UserDoctor.objects.get(user=user)

        if doctor.experience_years != '':
            words = ['год', 'года', 'лет']
            num = int(doctor.experience_years)
            years = decl_of_num(num, words)
            experience = 'Стаж: ' + str(num) + ' ' + years
        else:
            experience = ''

        _doctor = {
            'id': user.id,
            'fio': doctor_main.fio,
            'city': doctor_main.city,
            'phone': doctor_main.phone,
            'avatar': doctor_main.avatar,
            'specialty': doctor.specialty,
            'experience_years': experience
        }

        doctors.append(_doctor)

    data = {'doctors': doctors, 'page': page, 'users': users}

    return render(request, 'doctors_list.html', data)


def get_doctors_list(request):
    users = User.objects.filter(groups__name='doctors')
    doctors = list()

    for user in users:
        doctor_main = UserMain.objects.get(user=user)
        doctor = UserDoctor.objects.get(user=user)

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

        _doctor = {
            'id': user.id,
            'fio': doctor_main.fio,
            'city': doctor_main.city,
            'phone': doctor_main.phone,
            'avatar': avatar,
            'specialty': doctor.specialty,
            'experience_years': experience,
            'coords': doctor_main.coords,
        }

        doctors.append(_doctor)

    return HttpResponse(
        json.dumps(doctors),
        content_type="application/json"
    )


def create_meeting(request):
    if request.user.is_authenticated:
        date = request.GET['app-date']
        time = request.GET['app-time']
        doctor_id = request.GET['app-doctor-id']
        user_id = request.GET['app-user-id']
        title = 'Консультация'

        print(date)
        print(time)
        print(doctor_id)
        print(user_id)

        if date != '' and time != '' and doctor_id != '' and user_id != '':
            date_format = "%d.%m.%Y"
            date = datetime.strptime(date, date_format)
            date = date.strftime("%Y-%m-%d")
            meeting = Meeting.objects.create(title=title, date=date, time=time, doctor_id=doctor_id, user_id=user_id)
        try:
            meeting.save()
            result = 'ok'
        except:
            result = 'save err'
    else:
        result = 'auth err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


def get_calendar(request):
    if request.user.is_authenticated:

        if request.method == 'GET' and 'doctor_id' in request.GET:
            doctor_id = request.GET['doctor_id']
        else:
            doctor_id = request.user.id

        calendar_object_list = Calendar.objects.filter(doctor_id=doctor_id)
        calendar = list()

        for calendar_item in calendar_object_list:
            _calendar = {
                'id': calendar_item.id,
                'title': calendar_item.title,
                'date': str(calendar_item.date),
                'time_start': str(calendar_item.time_start),
                'time_end': str(calendar_item.time_end),
            }

            calendar.append(_calendar)

        result = calendar

    else:
        result = 'auth err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


def create_event(request):
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

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


def update_event(request):
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

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )


def delete_event(request):
    if request.user.is_authenticated:
        event_id = request.GET['event_id']

        instance = Calendar.objects.get(id=event_id)
        instance.delete()
        result = 'ok'
    else:
        result = 'auth err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )