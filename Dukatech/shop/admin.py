from django.contrib import admin
from .models import UserPaymentMethod, Product, Category

# Register your models here.
admin.site.register(UserPaymentMethod)
admin.site.register(Category)
admin.site.register(Product)
