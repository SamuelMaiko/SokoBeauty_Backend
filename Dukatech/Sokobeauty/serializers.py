from rest_framework import serializers
from .models import Post, User, comment, comment_replies, nested_replies
# 
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=["username", "email", "first_name", "last_name", "account_type"]
        
class PostSerializer(serializers.ModelSerializer):
    author=UserSerializer()
    comment_count=serializers.SerializerMethodField()
    likes_count=serializers.SerializerMethodField()
    
    
    class Meta:
        model=Post
        fields="__all__"
    
    def get_comment_count(self, obj):
        comment_count=obj.comments.count()
        return comment_count
    
    def get_likes_count(self, obj):
        likes_count=obj.likes.count()
        return likes_count
# repeated
class NestedRepliesChildrenSerializer(serializers.ModelSerializer):
    user=UserSerializer()   
     
    class Meta:
        model=nested_replies
        fields="__all__"


class NestedRepliesChildrenSerializer(serializers.ModelSerializer):
    user=UserSerializer()   
    nested_replies=NestedRepliesChildrenSerializer(many=True, read_only=True)
     
    class Meta:
        model=nested_replies
        fields="__all__"

class NestedRepliesChildrenSerializer(serializers.ModelSerializer):
    user=UserSerializer()   
    nested_replies=NestedRepliesChildrenSerializer(many=True, read_only=True)
     
    class Meta:
        model=nested_replies
        fields="__all__"
# Always repeat this for more nests
class NestedRepliesChildrenSerializer(serializers.ModelSerializer):
    user=UserSerializer()   
    nested_replies=NestedRepliesChildrenSerializer(many=True, read_only=True)
     
    class Meta:
        model=nested_replies
        fields="__all__"

    
class NestedRepliesChildrenSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    nested_replies=NestedRepliesChildrenSerializer(many=True, read_only=True)
    class Meta:
        model=nested_replies
        fields="__all__"

class NestedRepliesSerializer(serializers.ModelSerializer):
    nested_replies=NestedRepliesChildrenSerializer(many=True, read_only=True)
    user=UserSerializer()
    class Meta:
        model=nested_replies
        fields="__all__"

class CommentRepliesSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    nested_replies=NestedRepliesSerializer(many=True, read_only=True)
    class Meta:
        model=comment_replies
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    replies=CommentRepliesSerializer(many=True, read_only=True)
    likes_count=serializers.SerializerMethodField()
    replies_count=serializers.SerializerMethodField()
    
    class Meta:
        model=comment
        fields="__all__"

    def get_likes_count(self, obj):
        likes_count=obj.likes.count()
        return likes_count

    def get_replies_count(self, obj):
        replies_count=obj.replies.count()
        return replies_count
    
    
    
    # Next task is to :
        # likes_count on nested replies,
        # replies_count on nested replies,
        # like nested replies,