from django.db import models
from Sokobeauty.models import User

# Represents the various payment methods supported by the app
class PaymentMethod(models.Model):
    # user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    name=models.CharField(max_length=50)
    description=models.TextField()
    gateway_id = models.CharField(max_length=100)
    supported_currencies = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='payment_methods'
    
    def __str__(self):
        return self.name
    
# Represents the payment methods a user supports
class UserPaymentMethod(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_payment_mathods")
    payment_method=models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name="user_payment_methods")
    is_default=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='user_payment_methods'
        unique_together = ('user', 'payment_method')
    
    def __str__(self):
        return f"{self.user.username} has {self.payment_method.name}"
    

class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField(upload_to='logos/', default='product_categories/default.jpeg', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='categories'
        
    def __str__(self):
        return f"{self.name} category"
     
     
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField(upload_to='product_images/', default='product_images/default.jpeg', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_available=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='products'
        
    def __str__(self):
        return f"{self.name}"

# shopping cart
class Cart(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products=models.ManyToManyField(Product, through="CartItem", related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='carts'
        
    def __str__(self):
        return f"{self.user.username}'s cart "
    
# Association table representing a single item in a cart   
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='cart_items'
        unique_together=["cart", "product"]
        
    def __str__(self):
        return f"{self.cart.pk}'s and {self.product.name}'s cartItem"

# Order placed after checkout process
class Order(models.Model):
    
    ORDER_CHOICES=[
        ("PENDING","pending"),
        ("PROCESSING","processing"),
        ("SHIPPED","shipped"),
        ("DELIVERED","delivered"),
    ]
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status=models.CharField(max_length=50, choices=ORDER_CHOICES)
    shipping_address = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='orders'
        
    def __str__(self):
        return f"{self.user.username}'s order {self.pk}"
        
# Association table representing a single item in an order   
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity=models.IntegerField()
    item_price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='order_items'
        
    def __str__(self):
        return f"{self.order.pk}'s and {self.product.name}'s OrderItem"
    
# Records all transactions
class Transaction(models.Model):
    STATUS_CHOICES=[
        ("PENDING","pending"),
        ("COMPLETED","completed"),
        ("FAILED","failed"),
        ("CANCELLED","cancelled"),
        ("REFUNDED","refunded"),
    ]
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transaction")
    payment_method=models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, related_name="transaction")
    status=models.CharField(max_length=50, choices=STATUS_CHOICES)
    amount= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table='transcations'
        
    def __str__(self):
        return f"{self.order.pk}'s transaction {self.pk}"