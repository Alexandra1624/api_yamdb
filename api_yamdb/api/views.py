from django.db.models import Avg
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from ..api_yamdb.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (...)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['pk'])
        if request.user.is_admin or request.user.is_superuser:
            self.perform_destroy(category)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, category):
        category.delete()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (...)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=kwargs['pk'])
        if request.user.is_admin or request.user.is_superuser:
            self.perform_destroy(genre)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, genre):
        genre.delete()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('reviews__score'))
    # permission_classes = (...)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return TitleWriteSerializer
        return TitleReadSerializer
