import json

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from userprofile.models import UserMain, UserDoctor, User


def doctors_view(request):
    data = {}
    return render(request, 'doctors.html', data)


def doctors_map_list(request):
    doctors = User.objects.filter(groups__name='doctors')
    result = list()

    for user in doctors:
        doctor = UserMain.objects.get(user=user)

        _doctor = {
            'id': doctor.id,
            'fio': doctor.fio,
            'city': doctor.city,
            'phone': doctor.phone,
            'coords': doctor.coords,
        }

        result.append(_doctor)

    return HttpResponse(
        json.dumps(result),
        content_type="application/json"
    )