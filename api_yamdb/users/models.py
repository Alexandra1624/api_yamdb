from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ME = 'me'

role_choices = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
]


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        help_text='Обязательное поле. До 150 символов. Буквы, цифры разрешены.',
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует'
        },
    )
    email = models.EmailField(max_length=255, unique=True, blank=False)
    role = models.CharField(choices=role_choices, default='user', max_length=9)
    bio = models.TextField(max_length=500, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    confirmation_code = models.TextField(null=True, blank=True)

    exclude = ('confirmation_code',)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = ADMIN
        elif self.role == ADMIN:
            self.is_staff = True
        else:
            self.is_staff = False

        super(User, self).save(*args, **kwargs)
