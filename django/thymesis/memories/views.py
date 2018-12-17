from django.shortcuts import render
from rest_framework import generics
from .models import Users, Posts, Comments
from .serializers import UsersSerializer, PostsSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework.views import status
from .models import Users
#import requests


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
            user_id=request.data["user"],
            title=request.data["title"],
            location=request.data["location"],
            summary=request.data["summary"],
            post_body=request.data["post_body"],
            uri=request.data["uri"],
            votes=request.data["votes"]
            
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
            user_password=request.data["user_password"],
            mobile_number=request.data["mobile_number"],
            is_active=request.data["is_active"],
            username=request.data["username"],
            home_page=request.data["home_page"],
            
        )

        #This shall be uncommented when deploying the prototype
        #response = requests.put('http://127.0.0.1:5000/add/creator', data={'email': request.data["user_email"],
         #                                            'name': request.data["firstname"],
          #                                           'nick': request.data["username"],
           #                                          'home_page': request.data["home_page"],
            #                                         'type': 'person',
             #                                        'id': 89
              #                                       }
               #                  )

        return Response(
            data=UsersSerializer(a_User).data,
            status=status.HTTP_201_CREATED
        )
