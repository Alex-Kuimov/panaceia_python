import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from userprofile.models import UserMain, UserDoctor, User
from .models import Meeting
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

    data = request.GET['app-date']
    time = request.GET['app-time']
    doctor_id = request.GET['app-doctor-id']
    user_id = request.GET['app-user-id']
    title = 'Консультация'

    dateString = data
    dateFormatter = "%d.%m.%Y"
    date = datetime.strptime(dateString, dateFormatter)

    data = date.strftime("%Y-%m-%d")

    meeting = Meeting.objects.create(title=title, data=data, time=time, doctor_id=doctor_id, user_id=user_id)

    try:
        meeting.save()
        result = 'ok'
    except:
        result = 'err'

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )