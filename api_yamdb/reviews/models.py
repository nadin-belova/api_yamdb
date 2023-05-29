from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username, validate_year


class Category(models.Model):
    name = models.CharField(
        'имя категории',
        max_length=settings.MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        max_length=settings.MAX_SLUG_LENGTH
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'имя жанра',
        max_length=settings.MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
        max_length=settings.MAX_SLUG_LENGTH
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=settings.MAX_NAME_LENGTH,
        db_index=True
    )
    year = models.SmallIntegerField(
        'год',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    email = models.EmailField(
        verbose_name='Почта',
        unique=True
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=settings.MAX_USERNAME_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        choices=ROLE,
        max_length=50,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        'Текст'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(1, 'Приемлемые значения от 1 до 10'),
            MaxValueValidator(10, 'Приемлимые значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        'Отзыв',
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.username


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.username
