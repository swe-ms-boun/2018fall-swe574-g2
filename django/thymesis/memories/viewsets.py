from rest_framework import viewsets, filters
from .models import Posts,Users,Comments
from .serializers import PostsSerializer, UsersSerializer,CommentsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,) 
    search_fields=( 'firstname', 'lastname', 'username')

class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = (filters.SearchFilter,) 
    search_fields=(  'title', 'summary', 'body')

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = (filters.SearchFilter,) 
    search_fields=('comment_id','post', 'user')