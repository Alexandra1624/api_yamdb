<<<<<<< HEAD
from django.core.validators import MinValueValidator
from django.db import models

from .validators import current_year_validator
=======
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from users.models import User   # Определиться с названиями

from django.core.validators import MinValueValidator
>>>>>>> feature/review


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Адрес в URL - category/', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name[:20]


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Адрес в URL - genres/', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-name',)

    def __str__(self):
        return self.name[:20]


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=100)
    year = models.PositiveIntegerField(
        'Дата выхода произведения',
        db_index=True,
<<<<<<< HEAD
        validators=(
            MinValueValidator(1500),
            current_year_validator
        ),
=======
>>>>>>> feature/review
    )
    rating = models.IntegerField('Рейтинг', null=True)
    description = models.CharField(
        'Описание произведения', max_length=1000, null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:20]
<<<<<<< HEAD
=======


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,  # проверить
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'

    def __str__(self):
        return self.text[:100]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,   # название
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:100]
>>>>>>> feature/review