from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from Sokobeauty.models import Reply  
from django.conf import settings

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
    # ForeignKey to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    # ForeignKey to the Post model
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    # Timestamp for when the like is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensuring that each user can only like a specific post once
        unique_together = ('user', 'post')

    def __str__(self):
        # String representation of the Like instance
        return f"{self.user.username} likes {self.post.id}"

class comment(models.Model):
    # ForeignKey to link to the User model, representing the author of the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # ForeignKey to link to the Post model, representing the post on which the comment is made
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    # The content of the comment
    content = models.TextField()

    # Timestamp for when the comment is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp for when the comment is last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"
    
    


class comment_replies(models.Model):
    comment_id = models.ForeignKey(comment, on_delete=models.CASCADE, related_name='replies')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Reply by {self.author.username} on Comment {self.comment.id}'

class comment_like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment_id = models.ForeignKey(comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure each user can like a comment only once
        unique_together = ('user_id', 'comment_id')
    def __str__(self):
        return f'{self.user_id.username} likes Comment {self.comment_id.id}'
        
    
# class replies_likes(models.Model):  # Renamed from replies_likes for consistency
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reply_likes')
#     reply = models.ForeignKey('Sokobeauty.Reply', on_delete=models.CASCADE, related_name='likes')  # String-based reference
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'reply')

#     def __str__(self):
#         return f'{self.user} likes {self.reply}'

   
    
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Ensures a user can only follow another user once

    def __str__(self):
        return f'{self.follower} follows {self.following}'