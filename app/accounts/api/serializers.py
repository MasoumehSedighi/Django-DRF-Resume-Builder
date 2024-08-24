"""
Serializers for the user API View.
"""
from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer to manage extra user info"""

    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'about_me']


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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
