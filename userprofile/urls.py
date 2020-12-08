from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/info/', views.profile_page_view, name='user_profile'),
    path('profile/signup_user/', views.signup_user_view, name="signup_user"),
    path('profile/signup_doctor/', views.signup_doctor_view, name="signup_doctor"),
    path('profile/logout/', views.logout_view, name='logout'),
    path('profile/login/', views.login_view, name='login'),
    path('profile/main/', views.profile_page_view, name='user_profile_main'),
    path('profile/doctor/', views.profile_page_view, name='user_profile_doctor'),
    path('profile/recomend/', views.profile_page_view, name='user_profile_recomend'),
    path('profile/grafik/', views.profile_page_view, name='user_profile_grafik'),
    path('profile/consalt/', views.profile_page_view, name='user_profile_consalt'),
    path('profile/settings/', views.profile_page_view, name='user_profile_settings'),
    path('profile/videos/', views.profile_page_view, name='user_profile_videos'),
    path('save_main_data', views.save_main_data, name='save_main_data'),
    path('save_doctor_data', views.save_doctor_data, name='save_doctor_data'),
]