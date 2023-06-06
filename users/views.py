from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from users.models import CustomToken
from django.contrib.auth.models import User

from users.serializers import LoginSerializer, SignupSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import random
import string
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfile


class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        auth_user = None
        if user is not None:
            user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)

            # Create a new token for the user
            new_token = CustomToken.objects.create(user=user)

            return Response({'token': new_token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Delete all tokens for the current user
        CustomToken.objects.filter(user=request.user).delete()

        # Logout the user
        logout(request)

        return Response({'message': 'Logout successful'})


def generate_username(first_name):
    # Replace spaces with underscores
    username = first_name.replace(' ', '_')

    # Generate 6 random digits
    random_digits = ''.join(random.choices(string.digits, k=6))

    # Append random digits to the username
    username += random_digits

    return username


class SignUpView(APIView):
    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_profile = UserProfile(**serializer.validated_data)
            user_profile.username = generate_username(user_profile.first_name)
            user_profile.set_password(serializer.validated_data['password'])
            user_profile.save()
        return Response(status=status.HTTP_201_CREATED)
