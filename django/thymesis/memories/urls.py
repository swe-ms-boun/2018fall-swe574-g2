from django.urls import path
from memories.views import ListCommentsView, ListPostsView, ListUsersView


urlpatterns = [
    path('users/', ListUsersView.as_view(), name="users-all"),
    path('memories/', ListPostsView.as_view(), name="memories-all"),
    path('memories/posts', ListCommentsView.as_view(), name="comments-all")
]

