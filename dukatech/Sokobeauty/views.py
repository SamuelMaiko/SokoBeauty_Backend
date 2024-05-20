from django.shortcuts import render
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view 
from .models import Post
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def ShowAllPosts(request):
    posts=Post.objects.all()
    serializer=PostSerializer(posts, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def PostComments(request, post_id):
    post=Post.objects.filter(pk=post_id).first()
    if post:
        comments=post.comments
        serializer=CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    else:
        message=dict(error="Post does not exist!")
        return JsonResponse(message, safe=False, status=status.HTTP_404_NOT_FOUND)
        
        
        
    
