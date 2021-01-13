from django.urls import path
from . import views

urlpatterns = [
    path('get_calendar/', views.get_calendar, name='get_calendar'),
    path('create_event/', views.create_event, name='create_event'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('map/', views.doctors_map_view, name='doctors_map'),
    path('list/', views.doctors_list_view, name='doctors_list'),
    path('list/create_meeting/', views.create_meeting, name='create_meeting'),
    path('map/get_doctors_list/', views.get_doctors_list, name='get_doctors_map_list'),
]