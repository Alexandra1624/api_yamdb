from django.utils.crypto import random
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from users.emails import send_confirmation_code_via_email
from users.models import User

from .serializers import UserSerializer, SignUpSerializer, VerificationSerializer, CheckMeSerializer


class SignUpAPIView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=False)
        confirmation_code = random.randint(1000, 9999)
        if serializer.is_valid():
            serializer.save(confirmation_code=confirmation_code)
            send_confirmation_code_via_email(serializer.validated_data['email'])
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@action(detail=True, gmethods=['post'])
class VerifyAPIView(GenericAPIView):
    serializer_class = VerificationSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            return Response(
                {'token': serializer.data['token']}, status=status.HTTP_200_OK
            )
        elif serializer.errors.get('username') is not None:
            for error in serializer.errors.get('username'):
                if error.code == 'invalid':
                    return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = CheckMeSerializer(user, many=False, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
