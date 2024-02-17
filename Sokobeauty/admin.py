from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User
from .models import UserProfile
from .models import HairdresserProfile
from .models import Post
from .models import post_like
from .models import comment
from .models import comment_like
from .models import comment_replies
from .models import comment_replies_like
from .models import Booking
from .models import Follow
from .models import Review


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(HairdresserProfile)
admin.site.register(Post)
admin.site.register(post_like)
admin.site.register(comment)
admin.site.register(comment_replies)
admin.site.register(Booking)
admin.site.register(comment_like)
admin.site.register(Follow)
admin.site.register(Review)
admin.site.register(comment_replies_like)
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hairdresser', 'price', 'created_at', 'updated_at')
    list_filter = ('hairdresser', 'created_at')
    search_fields = ('name', 'description')
    
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_method', 'transaction_id', 'status', 'created_at', 'updated_at']
    list_filter = ['payment_method', 'status']
    search_fields = ['booking__id', 'transaction_id']