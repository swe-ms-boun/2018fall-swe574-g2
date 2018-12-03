from rest_framework import serializers
from memories import models

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = ('id', 'firstname', 'lastname', 'user_email', 'user_password')


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Posts
        fields = ('id', 'user_id', 'uri', 'title', 'summary', 'post_body', 'post_datetime', 'votes')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = ('id', 'post_id', 'user_id', 'comment_body', 'comment_datetime')