from django.shortcuts import render


def doctors_view(request):
    data = {}
    return render(request, 'doctors.html', data)