"""
Views for user API.
"""
from rest_framework import generics
from .serializers import RegisterSerializer


class RegisterUserView(generics.CreateAPIView):
    """Register a new user in the system."""
    serializer_class = RegisterSerializer
