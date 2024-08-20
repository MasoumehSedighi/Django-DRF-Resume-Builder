"""
Serializers for the user API View.
"""
from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
)


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer with password checkup"""

    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )
    password1 = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password1']

    def validate(self, data):
        if data['password'] != data["password1"]:
            raise serializers.ValidationError(
                {"detail": "passwords do not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password1")
        return get_user_model().objects.create_user(**validated_data)
