from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctors_view, name='doctors'),
    path('map_list/', views.doctors_map_list, name='map_list'),
]