from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model with email and password fields.
    """

    class Meta:
        """
        Meta class defining the model and fields for serialization.
        """

        model = User
        fields = ["email", "first_name","last_name"]
