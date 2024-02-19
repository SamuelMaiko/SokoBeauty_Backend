# from django.dispatch import receiver, Signal
# from .models import post_like, Post
# from django.db.models.signals import post_save


# update_likes_count=Signal()

# @receiver(post_save,sender=post_like)
# def update_likes(sender, instance, **kwargs):
#     # post_id=kwargs["post_id"]
#     instance.post.like_count=1
#     instance.save()
#     # specific_post=Post.objects.get(pk=post_id)
#     # if specific_post:
#     #     specific_post.like_count=1
#     #     specific_post.save()
#     #     print(f"likes updated for post {post_id}")