from django.contrib import admin
from django.urls import path 
from .views import register,login_user, dashboard,signup,getExpense,addExpense,delete_expense,getuserdata,otpverify,otp
urlpatterns = [

    path('register/',register),
    path('loguser/',login_user),
    path('dashboard/',dashboard),
    path('signup/',signup),
    path('getuserdata/',getuserdata),
    path('getexpense/',getExpense),
    path('addexpense/',addExpense),
    path('otpverification/',otpverify),
    path('otp/',otp),

    path('deleteexpense/<int:expense_id>/',delete_expense),
]
