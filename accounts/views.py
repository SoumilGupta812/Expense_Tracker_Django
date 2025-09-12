from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from .models import User ,Expense
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
from django.core.mail import send_mail
SECRET_KEY = "iamsecretkey" 
# Create your views here.
@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({
            "error":"Wrong method"
        })

    
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
        try:
            send_mail(
                        subject="Welcome to ExpenseTracker!",
                        message=f"Hi {username},\n\nThank you for registering at ExpenseTracker. Start tracking your expenses now!",
                        from_email=None,  # Uses DEFAULT_FROM_EMAIL
                        recipient_list=[email],
                        fail_silently=False,
                    )
        except Exception as e:
                print("Email sending failed:", e)
                # return redirect("userauths:home")
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
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

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
def getExpense(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")  # ✅ Extract user_id from token
        if not user_id:
            return JsonResponse({"error": "Invalid token payload"}, status=401)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # ✅ Only fetch posts belonging to this user
    expenses = list(
        Expense.objects.filter(user_id=user_id).values(
            "id", "expense_name", "amount"
        )
    )

    return JsonResponse(expenses, safe=False)
@csrf_exempt
def addExpense(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")  # ✅ Extract user_id from token
        if not user_id:
            return JsonResponse({"error": "Invalid token payload"}, status=401)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
    if request.method != 'POST':
        return JsonResponse({
            "error":"Wrong method"
        })

    
    data = json.loads(request.body)
    expense = data.get('expense')
    amount = data.get('amount')

    exp=Expense(user_id=user_id,expense_name=expense,amount=amount)
    exp.save()
    return JsonResponse({
            "message":"Expense has been added successfully",
            "status":True
            })
@csrf_exempt
def delete_expense(request, expense_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Wrong method"}, status=405)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    token = auth_header.split(" ")[1]  
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")  # ✅ Extract user_id from token
        if not user_id:
            return JsonResponse({"error": "Invalid token payload"}, status=401)
        try:
            expense = Expense.objects.get(id=expense_id, user_id=user_id)
            expense.delete()
            return JsonResponse({"message": "Expense deleted","status":True})
        except Expense.DoesNotExist:
            return JsonResponse({"error": "Expense not found"}, status=404)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
@csrf_exempt
def getuserdata(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")  # ✅ Extract user_id from token
        if not user_id:
            return JsonResponse({"error": "Invalid token payload"}, status=401)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)  
    # ✅ Only fetch posts belonging to this user
    user =User.objects.get(id=user_id)
    return JsonResponse({"username": user.username})

        
