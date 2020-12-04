from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup_user/', views.signup_user_view, name="signup_user"),
    path('accounts/signup_doctor/', views.signup_doctor_view, name="signup_doctor"),
    path('accounts/login/', views.login_view, name="login"),
    path('profile/', views.user_profile, name = 'user_profile'),
    path('main/', views.user_profile_main, name = 'user_profile_main'),
    path('recomend/', views.user_profile_recomend, name = 'user_profile_recomend'),
    path('grafik/', views.user_profile_grafik, name = 'user_profile_grafik'),
    path('consalt/', views.user_profile_consalt, name = 'user_profile_consalt'),
    path('settings/', views.user_profile_settings, name = 'user_profile_settings'),
    path('videos/', views.user_profile_videos, name = 'user_profile_videos'),
    path('save_main_data', views.save_main_data, name = 'save_main_data'),
]