from django.contrib import admin
from django.urls import path 
from .views import register,login_user, dashboard,signup,getExpense,addExpense
urlpatterns = [

    path('register/',register),
    path('loguser/',login_user),
    path('dashboard/',dashboard),
    path('signup/',signup),
    path('getexpense/',getExpense),
    path('addexpense/',addExpense),
]
