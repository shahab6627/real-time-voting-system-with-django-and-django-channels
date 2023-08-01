from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('register', register, name="register"),
    path('login', loginuser, name="login"),
    path('profile', profile, name="profile"),
    path('election-competition/<str:slug>', election_competition, name="election-competition"),
    path('logout', logout_user, name="logout")
    

]
