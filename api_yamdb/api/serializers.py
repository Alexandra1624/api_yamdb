from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from api.validators import check_username
from users.models import ADMIN, ME

from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Comment, Review


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


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    rating = serializers.FloatField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context.get('title_id')
        if (Review.objects.filter(author=author, title=title_id).exists()
                and self.context['request'].method != 'PATCH'):
            raise serializers.ValidationError('У вас уже есть отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
