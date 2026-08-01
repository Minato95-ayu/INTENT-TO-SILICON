
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
