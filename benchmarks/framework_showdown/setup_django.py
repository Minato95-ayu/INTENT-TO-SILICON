import os
import sys

def create_django_app():
    os.system("python -m django startproject config benchmarks/framework_showdown/django_app")
    
    views_code = """
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, User
import jwt
import json
import datetime

SECRET_KEY = "benchmark_secret"

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.filter(email=data.get('email'), password=data.get('password')).first()
        if user:
            exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            token = jwt.encode({"sub": user.email, "role": user.role, "exp": exp}, SECRET_KEY, algorithm="HS256")
            return JsonResponse({"success": True, "token": token})
        return JsonResponse({"detail": "Invalid Credentials"}, status=401)
    return JsonResponse({}, status=405)

def verify_admin(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") != "admin":
            return False
        return True
    except:
        return False

@csrf_exempt
def products(request):
    if request.method == 'GET':
        prods = Product.objects.all().values()
        return JsonResponse([p for p in prods], safe=False)
    
    if request.method == 'POST':
        if not verify_admin(request):
            return JsonResponse({"detail": "Forbidden"}, status=403)
        data = json.loads(request.body)
        p = Product.objects.create(name=data['name'], price=data['price'], stock=data['stock'])
        return JsonResponse({"id": p.id, "name": p.name, "price": p.price, "stock": p.stock})

@csrf_exempt
def product_detail(request, pid):
    if request.method == 'GET':
        p = Product.objects.filter(id=pid).values().first()
        if p:
            return JsonResponse(p)
        return JsonResponse({"detail": "Not Found"}, status=404)
"""
    models_code = """
from django.db import models

class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
"""
    
    urls_code = """
from django.urls import path
from api import views

urlpatterns = [
    path('api/login', views.login),
    path('api/products', views.products),
    path('api/products/<int:pid>', views.product_detail),
]
"""

    os.system("cd benchmarks/framework_showdown/django_app && python manage.py startapp api")
    
    with open("benchmarks/framework_showdown/django_app/api/views.py", "w") as f:
        f.write(views_code)
    
    with open("benchmarks/framework_showdown/django_app/api/models.py", "w") as f:
        f.write(models_code)
        
    with open("benchmarks/framework_showdown/django_app/config/urls.py", "w") as f:
        f.write(urls_code)
        
    # Inject api into INSTALLED_APPS
    with open("benchmarks/framework_showdown/django_app/config/settings.py", "a") as f:
        f.write("\nINSTALLED_APPS.append('api')\n")
        
    os.system("cd benchmarks/framework_showdown/django_app && python manage.py makemigrations api")
    os.system("cd benchmarks/framework_showdown/django_app && python manage.py migrate")
    print("Django App Setup Complete")

if __name__ == "__main__":
    create_django_app()
