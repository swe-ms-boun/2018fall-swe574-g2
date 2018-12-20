from rest_framework import routers
from memories.viewsets import UserViewSet, PostViewSet, CommentViewSet

router = routers.DefaultRouter()

router.register(r'Users', UserViewSet)
router.register(r'Posts', PostViewSet)
router.register(r'Comments',CommentViewSet)