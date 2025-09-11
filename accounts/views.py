from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
SECRET_KEY = "iamsecretkey" 
# Create your views here.
@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({
            "error":"Wrong method"
        })
    print("hello")
    
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    try:
        if not username or not email or not password:
           return JsonResponse({
            "error":"All Fields are Required"
            })
        if User.objects.filter(username=username).exists():
             return JsonResponse({
            "error":"User Already Exist"
            }) 
        
        if User.objects.filter(email=email).exists():
             return JsonResponse({
            "error":"User Already Exist"
            }) 
        user  = User(username=username,email=email,password=make_password(password))
        user.save()
        return JsonResponse({
            "message":"User has been created successfully",
            "status":True
            })
    
    except Exception as e:
      return JsonResponse({
          "error":e
      }) 
    
@csrf_exempt
def login_user(request):
    print("hello")
    if request.method != 'POST':
        return JsonResponse({"error": "Wrong method"})

    
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            payload = {
                "id": user.id,
                "username": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) # token expiry
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return JsonResponse({"token": token, "status": True})
        else:
            return JsonResponse({"error": "Invalid password"})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"})
    
def dashboard(request):
    return render(request,'dashboard.html')
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')