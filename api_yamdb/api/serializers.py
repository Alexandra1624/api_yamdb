from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from api.validators import check_username
from users.models import ADMIN, ME


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {'email': {'required': True}}
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def validate(self, data):
        if data['username'] == ME:
            raise serializers.ValidationError("Имя me недопустимо!")
        return data


class VerificationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[check_username])
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token')

    @staticmethod
    def get_token(data):
        token = RefreshToken.for_user(
            User.objects.get(username=data['username'])
        )
        access = token.access_token
        return str(access)

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        conf_code = User.objects.get(username=data['username']).confirmation_code
        if confirmation_code is None:
            raise serializers.ValidationError(
                'A confirmation_code is required to log in.'
            )
        elif confirmation_code != conf_code:
            raise serializers.ValidationError(
                'Confirmation code is invalid'
            )
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('username', 'email', 'username', 'first_name', 'last_name',
                  'bio', 'role')


class CheckMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta(object):
        model = User
        fields = ('username', 'email', 'username', 'first_name', 'last_name',
                  'bio', 'role')

    def validate(self, data):
        instance = getattr(self, 'instance')
        if instance.role != ADMIN:
            data['role'] = instance.role
        return data
