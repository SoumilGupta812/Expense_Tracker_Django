from django.contrib import admin
from django.urls import path 
from .views import register,login_user, dashboard,signup
urlpatterns = [

    path('register/',register),
    path('loguser/',login_user),
    path('dashboard/',dashboard),
    path('signup/',signup),
]
