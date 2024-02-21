from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from Sokobeauty.models import Reply  
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# from Sokobeauty.models import User

class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('vendor', 'Vendor'),
        ('hairdresser', 'Hairdresser'),
    ]

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='normal')
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Ensure email is saved in lowercase
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    # One-to-one link to Django's built-in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Additional fields
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username  # Assum
    
class HairdresserProfile(models.Model):
    # Primary key for the HairdresserProfile model
    hairdresser_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hairdresser_profile')
    salon_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='hairdresser_profiles/', null=True, blank=True)
    address = models.TextField()  # Address that can be viewed on a map
    description = models.TextField()
    services_offered = models.TextField()  # List of services offered
    website = models.URLField(null=True, blank=True)  # Link to the website
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.salon_name
    
class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    is_booking = models.BooleanField(default=False)
    is_purchasing = models.BooleanField(default=False)
    content = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.username} on {self.created_at.strftime('%Y-%m-%d')}"
    
class post_like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.id} is {self.post.image}"

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"
    


class comment_replies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    parent_comment = models.ForeignKey(comment, on_delete=models.CASCADE, null =True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        parent_comment_str = ''
        if self.parent_comment:
            parent_comment_str = f' (nested under {self.parent_comment})'
        return f'{self.user.username}: {self.content}{parent_comment_str}'

    def __str__(self):
        return f'Reply by {self.user.username} on Reply {self.parent_comment.id}'
        # if self.parent_comment:
        #     return f'Reply by {self.user.username} on Comment {self.parent_comment.id}'
        # else:
        #     return f'Reply by {self.user.username} on Reply {self.parent_reply.id}'
        
        
class nested_replies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_nested_replies')
    parent_reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='nested_replies')
    comment_reply = models.ForeignKey(comment_replies, null=True, blank=True, on_delete=models.CASCADE, related_name='nested_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
    # Ensure that a reply is only nested under a comment reply or another reply, not both
        if self.parent_reply and self.comment_reply:
            raise ValidationError('A reply cannot be both a nested reply and a comment reply at the same time.')

    def __str__(self):
        parent_reply_str = ''
        if self.parent_reply:
            parent_reply_str = f' (nested under {self.parent_reply.user.username})'
        return f'{self.user.username}: {self.content}{parent_reply_str}'

class nested_replies_likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nested_reply_likes')
    nested_reply = models.ForeignKey('nested_replies', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'nested_reply')  

    def __str__(self):
        return f'{self.user.username} likes Nested Reply {self.nested_reply.id}'
    
    
class comment_like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment_id = models.ForeignKey(comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'comment_id')
    def __str__(self):
        return f'{self.user_id.username} likes Comment {self.comment_id.id}'
        
class comment_replies_like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reply_likes')
    reply = models.ForeignKey(comment_replies, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reply')  

    def __str__(self):
        return f'{self.user.username} likes Reply {self.reply.id}'


    
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Ensures a user can only follow another user once

    def __str__(self):
        return f'{self.follower} follows {self.following}'
    
    
class Service(models.Model):
    hairdresser = models.ForeignKey('HairdresserProfile', on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='services/images/', blank=True, null=True)
    videos = models.FileField(upload_to='services/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    hairdresser = models.ForeignKey('HairdresserProfile', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='bookings')
    booking_time = models.DateTimeField()  # Example field, adjust according to your needs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} booking with {self.hairdresser.salon_name} for {self.service.name} on {self.booking_time.strftime('%Y-%m-%d %H:%M')}"
    
    
class Cancellation(models.Model):
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='cancellation')
    reason = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_status = models.CharField(max_length=8, choices=REFUND_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Cancellation for Booking ID {self.booking_id} - Status: {self.refund_status}"
    
    
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Booking ID {self.booking_id} - {self.amount} - {self.status}"
    
    
class Review(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_reviews')
    hairdresser = models.ForeignKey('HairdresserProfile', on_delete=models.CASCADE, related_name='hairdresser_reviews')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='service_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.hairdresser.salon_name}"




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