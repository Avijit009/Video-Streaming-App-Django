from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),
    path('profile/', views.user_profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('password/', views.pass_change, name='update_password'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
]