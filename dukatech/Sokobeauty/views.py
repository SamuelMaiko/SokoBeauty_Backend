from django.shortcuts import render

from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

from .models import Product
from .serializers import ProductSerializer ,ProductCreateSerializer,CategoryProductSerializer

# categories and products

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    
class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CategoryProductListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer
    
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
# carts
    
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer

# authenticated users

class SpecificCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        # Attempt to retrieve the authenticated user's cart
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CartDetailView(APIView):
    def get(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
# ORDER AND ITEMS
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, OrderItemSerializer

class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
# order for autthenticated user
# class OrderListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

# class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
    
    
class UserOrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all orders
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)

class UserOrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view returns an order for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)