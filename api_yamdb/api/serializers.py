from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'last_name',
            'first_name',
            'bio',
            'role'
        ]


class UserMeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CodeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        validators=[validate_username],
        max_length=settings.MAX_USERNAME_LENGTH
    )


class GetTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(
        required=True,
        max_length=settings.MAX_USERNAME_LENGTH
    )
    confirmation_code = serializers.SlugField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Вы не можете добавить более'
                                  'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
