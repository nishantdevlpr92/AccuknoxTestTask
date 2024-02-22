from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from user_hub.models import Friends


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


class FriendDataSerializer(serializers.ModelSerializer):
    receiver_user = SearchUserSerializer()
    sender_user = SearchUserSerializer()

    class Meta:
        model = Friends
        fields = ["id", "receiver", "sender_user", "receiver_user", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["receiver"].required = True
        for field_name in self.fields.keys():
            if field_name != "receiver":
                self.fields[field_name].required = False