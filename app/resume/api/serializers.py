"""
Serializers for resume APIs.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from resume.models import (
    Skill,
    Education,
    Certificate,
    Experience
)
from accounts.api.serializers import ProfileSerializer


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills."""

    class Meta:
        model = Skill
        fields = ['id', 'user', 'title']
        read_only_fields = ['id', 'user']


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for educations."""

    class Meta:
        model = Education
        fields = [
            'id',
            'user',
            'institution',
            'degree',
            'start_date',
            'end_date'
        ]
        read_only_fields = ['id', 'user']

    def validate(self, data):
        """
        Validate end date
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date and start_date > end_date:
            raise serializers.ValidationError(
                "Start date must be before the end date."
            )

        return data


class CertificateSerializer(serializers.ModelSerializer):
    """Serializer for Certificate"""

    class Meta:
        model = Certificate
        fields = [
            'id',
            'user',
            'title',
            'issuing_organization',
            'issue_date'
        ]
        read_only_fields = ['id', 'user']


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for Experience"""
    class Meta:
        model = Experience
        fields = [
            'id',
            'user',
            'company',
            'position',
            'description',
            'start_date',
            'end_date'
        ]
        read_only_fields = ['id', 'user']

    def validate(self, data):
        """
        Validate end date
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date and start_date > end_date:
            raise serializers.ValidationError(
                "Start date must be before the end date."
            )

        return data


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for all Resume"""

    profile = ProfileSerializer()
    skills = SkillSerializer(many=True)
    educations = EducationSerializer(many=True)
    certificates = CertificateSerializer(many=True)
    experiences = ExperienceSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            'profile',
            'email',
            'skills',
            'educations',
            'certificates',
            'experiences'
        ]
