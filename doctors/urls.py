from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctors_view, name='doctors'),
]