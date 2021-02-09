from django.urls import path
from . import views

urlpatterns = [
    path('get_calendar/', views.get_calendar, name='get_calendar'),
    path('create_event/', views.create_event, name='create_event'),
    path('update_event/', views.update_event, name='update_event'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('get_meetings/', views.get_meetings, name='get_meetings'),
    path('get_meeting/', views.get_meeting, name='get_meeting'),
    path('reject_meeting/', views.reject_meeting, name='reject_meeting'),
    path('archive_meeting/', views.archive_meeting, name='archive_meeting'),
    path('update_meeting/', views.update_meeting, name='update_meeting'),
    path('detail/<slug:slug>/', views.doctor_detail_view, name='doctor_detail'),
    path('map/', views.doctors_map_all_view, name='doctors_map_all'),
    path('map/<slug:slug>/', views.doctors_map_view, name='doctors_map'),
    path('list/', views.doctors_list_all_view, name='doctors_list_all'),
    path('list/<slug:slug>/', views.doctors_list_view, name='doctors_list'),
    path('create_meeting/', views.create_meeting, name='create_meeting'),
    path('get_doctors_list/', views.get_doctors_list, name='get_doctors_map_list'),
]