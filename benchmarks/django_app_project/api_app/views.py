from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"success": True, "data": {"status": "ok"}})

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()[:20]
        data = ProductSerializer(products, many=True).data
        return Response({
            "success": True,
            "data": data,
            "meta": {"total": Product.objects.count(), "page": 1, "limit": 20}
        })

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()[:20]
        data = OrderSerializer(orders, many=True).data
        return Response({
            "success": True,
            "data": data,
            "meta": {"total": Order.objects.count(), "page": 1, "limit": 20}
        })

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
