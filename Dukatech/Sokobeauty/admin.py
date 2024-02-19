from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User
from .models import UserProfile
from .models import HairdresserProfile
from .models import Post
from .models import post_like
from .models import comment_like
from .models import comment
from .models import comment_replies
# from .models import replies_like
from .models import Follow, VendorProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(HairdresserProfile)
admin.site.register(Post)
admin.site.register(post_like)
admin.site.register(comment)
admin.site.register(comment_replies)
# admin.site.register(replies_likes)
admin.site.register(comment_like)
admin.site.register(Follow)
admin.site.register(VendorProfile)