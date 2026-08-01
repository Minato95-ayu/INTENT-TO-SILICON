from django.urls import path
from .views import ProductListView, OrderListView, HealthCheckView
import jwt
import time
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

# Simple Mock Login to match FastAPI and AAYU flow
class LoginView(APIView):
    def post(self, request):
        payload = {
            "email": request.data.get("email"),
            "id": 1,
            "exp": int(time.time()) + 86400
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return Response({"success": True, "data": token})

urlpatterns = [
    path('api/products', ProductListView.as_view(), name='product-list'),
    path('api/orders', OrderListView.as_view(), name='order-list'),
    path('api/login', LoginView.as_view(), name='login'),
    path('health', HealthCheckView.as_view(), name='health'),
]
