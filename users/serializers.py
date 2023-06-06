from rest_framework import serializers
from users.models import UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=UserProfile.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    phone_number = serializers.CharField(
        required=True,
        max_length=16,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True}
        }
