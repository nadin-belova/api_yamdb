from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (AdminOrReadOnly, AuthenticatedOrReadOnly,
                             IsAdmin)
from api.serializers import (CategorySerializer, CodeEmailSerializer,
                             CommentSerializer, GenreSerializer,
                             GetTokenSerializer, ReviewSerializer,
                             TitlePostSerializer, TitleReadSerializer,
                             UserMeSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class LimitPutRequest(viewsets.ModelViewSet):

    http_method_names = ('get', 'post', 'patch', 'delete',)


class UserViewSet(LimitPutRequest):
    """
    Работа с пользователями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_and_confirmation_code(request):
    serializer = CodeEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user_email = User.objects.filter(email=email).first()
    user_username = User.objects.filter(username=username).first()
    if user_email != user_username:
        if user_email:
            return Response(
                {'message': f'Почта {email} уже используется.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'message': f'Имя {username} уже используется.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user, _ = User.objects.get_or_create(
        email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Код подтверждения: {confirmation_code}',
        settings.EMAIL_SENDER,
        [user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):

    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class TitleViewSet(LimitPutRequest):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleReadSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitlePostSerializer


class BaseListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(BaseListCreateDestroyViewSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseListCreateDestroyViewSet):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(LimitPutRequest):
    serializer_class = ReviewSerializer
    permission_classes = [AuthenticatedOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self, *args, **kwargs):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(LimitPutRequest):
    serializer_class = CommentSerializer
    permission_classes = [AuthenticatedOrReadOnly]

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
