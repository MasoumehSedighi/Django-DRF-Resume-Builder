"""
Serializers for resume APIs.
"""
from rest_framework import serializers
from resume.models import (
    Skill,
    Education,
)


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills."""

    class Meta:
        model = Skill
        fields = ['id', 'user', 'title']
        read_only_fields = ['user']


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for educations."""

    class Meta:
        model = Education
        fields = [
            'id', 'user', 'institution', 'degree', 'start_date', 'end_date'
        ]
        read_only_fields = ['user']

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
