from django.contrib import admin
from django.urls import path 
from .views import register,login_user, dashboard,signup,getExpense,addExpense,delete_expense
urlpatterns = [

    path('register/',register),
    path('loguser/',login_user),
    path('dashboard/',dashboard),
    path('signup/',signup),
    path('getexpense/',getExpense),
    path('addexpense/',addExpense),
    path('deleteexpense/<int:expense_id>/',delete_expense),
]
