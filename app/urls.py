from django.urls import path
from . import views

urlpatterns = [
    path('', views.Splash, name='splash'),
    path('register', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('home', views.Home, name='home'),
    path('logout', views.Logout, name='logout'),
]