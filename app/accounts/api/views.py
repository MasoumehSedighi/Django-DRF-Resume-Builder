"""
Views for user API.
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication, permissions
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    AuthTokenSerializer,
)
from accounts.models import Profile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class RegisterUserView(generics.CreateAPIView):
    """Register a new user in the system."""
    serializer_class = RegisterSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileUserView(generics.RetrieveUpdateAPIView):
    """Manage profile of authenticated user"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive and return the authenticated user's profile."""
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
