from django.shortcuts import render
from rest_framework import generics
from .models import Users, Posts, Comments
from .serializers import UsersSerializer, PostsSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework.views import status


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

class ListCreatePostsView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def post(self, request, *args, **kwargs):
        a_Post = Posts.objects.create(
            user_id=request.data["user_id"],
            title=request.data["title"],
            summary=request.data["summary"],
            post_body = request.data["post_body"],
            uri = request.data["uri"],
            votes = request.data["votes"]
            
        )
        return Response(
            data=PostsSerializer(a_Post).data,
            status=status.HTTP_201_CREATED
        )

class ListCreateUsersView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def post(self, request, *args, **kwargs):
        a_User = Users.objects.create(
            firstname=request.data["firstname"],
            lastname=request.data["lastname"],
            user_email=request.data["user_email"],
            user_password = request.data["user_password"],
            mobile_number = request.data["mobile_number"],
            is_active = request.data["is_active"]
            
        )
        return Response(
            data=UsersSerializer(a_User).data,
            status=status.HTTP_201_CREATED
        )