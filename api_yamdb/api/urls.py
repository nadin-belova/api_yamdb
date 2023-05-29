from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, TitleViewSet,
                    GenreViewSet, ReviewViewSet, UserViewSet, get_token,
                    signup_and_confirmation_code)


app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres',
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', signup_and_confirmation_code),
    path('token/', get_token),
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
