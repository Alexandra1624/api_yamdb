from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter, Route

from .views import (
    SignUpAPIView, UserViewSet, VerifyAPIView,
    CategoryViewSet, GenreViewSet, TitleViewSet,
    CommentViewSet, ReviewViewSet
)


class CustomCategoryGenreRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={
                'get': 'list',
                'post': 'create',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={
                'delete': 'destroy',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


router = SimpleRouter()
router_titles_v1 = DefaultRouter()
router_category_genre_v1 = CustomCategoryGenreRouter()
router_category_genre_v1.register(
    r'categories', CategoryViewSet, basename='category'
)
router_category_genre_v1.register(r'genres', GenreViewSet, basename='genre')
router_titles_v1.register(r'titles', TitleViewSet, basename='title')

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/auth/token/', VerifyAPIView.as_view(), name='verify_token'),
    path('v1/', include(router_titles_v1.urls)),
    path('v1/', include(router_category_genre_v1.urls)),
]
