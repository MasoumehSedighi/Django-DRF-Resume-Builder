from django.urls import path
from .views import (
    RegisterUserView,
    ProfileUserView,
    CreateTokenView,
)


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name='register'),
    path("profile/", ProfileUserView.as_view(), name='profile'),
    path("token/", CreateTokenView.as_view(), name='token'),
]
