from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.doctors_map_view, name='doctors_map'),
    path('list/', views.doctors_list_view, name='doctors_list'),
    path('list/create_meeting/', views.create_meeting, name='create_meeting'),
    path('map/get_doctors_list/', views.get_doctors_list, name='get_doctors_map_list'),
]