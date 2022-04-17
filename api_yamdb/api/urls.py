from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet

router_titles_v1 = routers.DefaultRouter()
router_titles_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_titles_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_titles_v1.urls)),
]
