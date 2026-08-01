
from django.urls import path
from api import views

urlpatterns = [
    path('api/login', views.login),
    path('api/products', views.products),
    path('api/products/<int:pid>', views.product_detail),
]
