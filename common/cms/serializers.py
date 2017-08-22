from django.contrib.auth import get_user_model
from rest_framework import serializers

UserBase = get_user_model()


class SuperUserSerializer(serializers.ModelSerializer):
    """
    Register a new superuser.
    Validates email and username.
    """
    email = serializers.EmailField(error_messages={
        "invalid": "ERROR_INVALID_EMAIL",
        "required": "ERROR_REQUIRED",
        "null": "ERROR_NULL",
        "blank": "ERROR_BLANK",
    })
    name = serializers.CharField(error_messages={
        "required": "ERROR_REQUIRED",
        "null": "ERROR_NULL",
        "blank": "ERROR_BLANK",
    })

    class Meta:
        model = UserBase
        fields = ('id', 'email', 'name', 'is_active')

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data['name']

        return UserBase.objects.create_superuser(username=email, email=email, is_email_verified=True, name=name)
