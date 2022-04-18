from django.urls import include, path
from rest_framework import routers

from .views import SignUpAPIView, UserViewSet, VerifyAPIView

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/auth/token/', VerifyAPIView.as_view(), name='verify_token')
]
