from django.urls import path, include
from . import views

urlpatterns=[
    path('posts/', views.ShowAllPosts, name="all-posts"),
    path('post-comments/<int:post_id>', views.PostComments, name="post-comments"),
    
]