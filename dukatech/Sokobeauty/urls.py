from django.urls import path
from .views import CategoryList, ProductList ,ProductCreateView, ProductDetailView ,ProductDeleteView,CategoryDetailView, CategoryProductListView , CartDetailView
from .views import SpecificCartView
from .views import OrderListCreateAPIView, OrderDetailAPIView, UserOrderDetailAPIView, UserOrderListAPIView

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='[product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('categoriesproducts/', CategoryProductListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('users/<int:user_id>/cart/', SpecificCartView.as_view(), name='specific-cart'),
    path('cart/<int:cart_id>/', CartDetailView.as_view(), name='cart-detail-view'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('orderswithuser/', UserOrderListAPIView.as_view(), name='user-orders'),
    path('orderswithuser/<int:pk>/', UserOrderDetailAPIView.as_view(), name='user-order-detail'),
]
