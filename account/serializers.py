from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer that extends TokenObtainPairSerializer.
    
    This serializer adds additional data to the token payload including user's email, id, first name, and last name.
    
    Attributes:
        Inherits from TokenObtainPairSerializer.
    
    Methods:
        get_token(cls, user): A class method that returns the token for the provided user.
            Args:
                cls: The class itself.
                user: The user object for which the token is being generated.
            Returns:
                Token: A JSON Web Token containing additional user data.
        
        validate(self, attrs): Validates the serializer's data and returns additional user information.
            Args:
                attrs: The data to be validated.
            Returns:
                dict: A dictionary containing user's email, id, first name, last name, and token.
    """

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['id'] = user.id
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['id'] = self.user.id
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data