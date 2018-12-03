from rest_framework import serializers
from memories import models

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ('id', 'firstname', 'lastname', 'user_email', 'username',
                  'home_page', 'user_password', 'mobile_number', 'is_active')


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Posts
        fields = ('id', 'user_id', 'uri', 'location', 'title', 'summary', 'post_body', 'post_datetime', 'votes')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = ('id', 'post_id', 'user_id', 'comment_body', 'comment_datetime')