"""
Serializers for resume APIs.
"""
from rest_framework import serializers
from resume.models import (
    Skill,
)


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills."""

    class Meta:
        model = Skill
        fields = ['id', 'user', 'title']
        read_only_fields = ['user']
