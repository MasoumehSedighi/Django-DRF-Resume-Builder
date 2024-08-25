"""
Views for the resume APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from resume.api import serializers
from resume.models import (
    Skill,
    Education
)


class SkillViewSet(viewsets.ModelViewSet):
    """view for manage skill APIs."""

    serializer_class = serializers.SkillSerializer
    queryset = Skill.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the skills for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class EducationViewSet(viewsets.ModelViewSet):
    """view for manage education APIs."""

    serializer_class = serializers.EducationSerializer
    queryset = Education.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the educations for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
