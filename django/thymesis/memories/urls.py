from django.urls import path
from memories.views import ListCommentsView, ListPostsView, ListUsersView, ListCreatePostsView, ListCreateUsersView


urlpatterns = [
    path('users/', ListUsersView.as_view(), name="users-all"),
    path('memories/get-all-memories', ListPostsView.as_view(), name="memories-all"),
    path('memories/comments/get-all-comments', ListCommentsView.as_view(), name="comments-all"),
    path('memories/create', ListCreatePostsView.as_view(), name="memory-list-create"),
    path('users/create', ListCreateUsersView.as_view(), name="user-create")

]

