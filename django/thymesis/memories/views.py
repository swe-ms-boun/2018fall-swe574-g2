from django.shortcuts import render
from rest_framework import generics
from .models import Users, Posts, Comments
from .serializers import UsersSerializer, PostsSerializer, CommentsSerializer

# Create your views here.
class ListUsersView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class ListPostsView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class ListCommentsView(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer