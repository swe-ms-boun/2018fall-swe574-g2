from django.shortcuts import render
from rest_framework import generics
from .models import Users, Posts, Comments
from .serializers import UsersSerializer, PostsSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework.views import status
from .models import Users
#import requests
