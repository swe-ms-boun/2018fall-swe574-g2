from rest_framework import serializers
from memories import models

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Posts
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comments
        fields = '__all__'