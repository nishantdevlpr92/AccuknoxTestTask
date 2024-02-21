from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model with email and password fields.
    """

    class Meta:
        """
        Meta class defining the model and fields for serialization.
        """

        model = User
        fields = ["email", "password", "first_name","last_name"]

    def validate_email(self, value):
        """
        Check if the email already exists in a case-insensitive manner.
        """

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def create(self, validated_data):
        """
        Create a new user instance with validated data.
        """

        user = User.objects.create_user(**validated_data)
        return user
