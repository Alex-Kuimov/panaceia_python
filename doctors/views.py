import json

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from userprofile.models import UserMain, UserDoctor, User


def doctors_map_view(request):
    data = {}
    return render(request, 'doctors_map.html', data)


def doctors_list_view(request):
    users = User.objects.filter(groups__name='doctors')
    doctors = list()

    for user in users:
        doctor_main = UserMain.objects.get(user=user)
        doctor = UserDoctor.objects.get(user=user)

        _doctor = {
            'id': doctor_main.id,
            'fio': doctor_main.fio,
            'city': doctor_main.city,
            'phone': doctor_main.phone,
            'avatar': doctor_main.avatar,
            'specialty': doctor.specialty,
            'experience_years': doctor.experience_years
        }

        doctors.append(_doctor)

    data = {'doctors': doctors}

    return render(request, 'doctors_list.html', data)


def get_doctors_list(request):
    users = User.objects.filter(groups__name='doctors')
    doctors = list()

    for user in users:
        doctor_main = UserMain.objects.get(user=user)
        doctor = UserDoctor.objects.get(user=user)

        if doctor_main.avatar != '':
            avatar = 'media/' + str(doctor_main.avatar)
        else:
            avatar = 'static/img/user.png'

        _doctor = {
            'id': doctor_main.id,
            'fio': doctor_main.fio,
            'city': doctor_main.city,
            'phone': doctor_main.phone,
            'avatar': avatar,
            'specialty': doctor.specialty,
            'experience_years': 'Стаж: ' + doctor.experience_years + ' лет',
            'coords': doctor_main.coords,
        }

        doctors.append(_doctor)

    return HttpResponse(
        json.dumps(doctors),
        content_type="application/json"
    )