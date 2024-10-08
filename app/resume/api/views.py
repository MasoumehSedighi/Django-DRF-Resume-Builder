"""
Views for the resume APIs.
"""
from rest_framework import (
    viewsets,
    generics,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from resume.api import serializers
from resume.models import (
    Skill,
    Education,
    Certificate,
    Experience
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


class CertificateViewSet(viewsets.ModelViewSet):
    """view for manage certificate APIs."""

    serializer_class = serializers.CertificateSerializer
    queryset = Certificate.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the certificates for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceViewSet(viewsets.ModelViewSet):
    """view for manage experience APIs."""

    serializer_class = serializers.ExperienceSerializer
    queryset = Experience.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the experiences for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ResumeAPIView(generics.RetrieveAPIView):
    """
    API view to retrieving all resume-related data for the authenticated user.
    """
    serializer_class = serializers.ResumeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
