from rest_framework import serializers
from memories import models

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ('user_id', 'firstname', 'lastname', 'user_email', 'username',
                  'home_page', 'user_password', 'mobile_number', 'is_active')


class PostsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Posts
        fields = ('post_id', 'user', 'uri', 'location', 'title', 'summary', 'post_body', 'post_datetime', 'votes')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = ('comment_id', 'post', 'user', 'comment_body', 'comment_datetime')