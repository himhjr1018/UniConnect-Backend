from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from users.models import CustomToken, Education, Experience, InterestedProgram
from django.contrib.auth.models import User

from users.serializers import LoginSerializer, SignupSerializer, AddEducationSerializer, AddExperienceSerializer, \
    AddInterestedProgramSerializer, EducationSerializer, ExperienceSerializer, InterestedProgramSerializer, \
    UploadProfilePicSerializer, EditIntroSerializer, UpdateUserNameSerializer, UserProfileDetailSerializer
from rest_framework import status, generics, permissions
from drf_yasg.utils import swagger_auto_schema
import random
import string
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfile
from rest_framework.parsers import MultiPartParser


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
        if serializer.is_valid():
            user_profile = UserProfile(**serializer.validated_data)
            user_profile.username = generate_username(user_profile.first_name)
            user_profile.set_password(serializer.validated_data['password'])
            user_profile.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddEducation(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=AddEducationSerializer)
    def post(self, request):
        serializer = AddEducationSerializer(data=request.data)
        if serializer.is_valid():
            profile = UserProfile.objects.get(id=request.user.id)
            serializer.save(profile=profile)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddExperience(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=AddExperienceSerializer)
    def post(self, request):
        serializer = AddExperienceSerializer(data=request.data)

        if serializer.is_valid():
            profile = UserProfile.objects.get(id=request.user.id)
            serializer.save(profile=profile)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterestedProgramCreateAPIView(generics.CreateAPIView):
    serializer_class = AddInterestedProgramSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = UserProfile.objects.get(id=self.request.user.id)
        serializer.save(profile=profile)


class EducationUpdateAPIView(generics.UpdateAPIView):
    allowed_methods = ['PUT']
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        education = self.get_object()
        if education.profile.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to edit this education.")
        serializer.save()


class ExperienceUpdateAPIView(generics.UpdateAPIView):
    allowed_methods = ['PUT']
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        experience = self.get_object()
        if experience.profile.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to edit this experience.")
        serializer.save()


class InterestedProgramUpdateAPIView(generics.UpdateAPIView):
    allowed_methods = ['PUT']
    queryset = InterestedProgram.objects.all()
    serializer_class = InterestedProgramSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        interested_program = self.get_object()
        if interested_program.profile.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to edit this interested program.")
        serializer.save(profile=interested_program.profile)


class EducationDeleteAPIView(generics.DestroyAPIView):
    queryset = Education.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.profile.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to delete this education instance.")
        instance.delete()


class ExperienceDeleteAPIView(generics.DestroyAPIView):
    queryset = Experience.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.profile.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to delete this experience instance.")
        instance.delete()


class InterestedProgramDeleteAPIView(generics.DestroyAPIView):
    queryset = InterestedProgram.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.profile.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to delete this interested program instance.")
        instance.delete()


class ProfilePictureUploadAPIView(generics.UpdateAPIView):
    allowed_methods = ['PATCH']
    queryset = UserProfile.objects.all()
    serializer_class = UploadProfilePicSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, ]

    def perform_update(self, serializer):
        serializer.save(profile_picture=self.request.FILES.get('profile_picture'))

    def get_object(self):
        return self.request.user.userprofile


class EditIntroAPIView(generics.UpdateAPIView):
    allowed_methods = ['PATCH']
    serializer_class = EditIntroSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


class UsernameUpdateAPIView(generics.UpdateAPIView):
    allowed_methods = ['PATCH']
    serializer_class = UpdateUserNameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True  # Allow partial updates
        return super().get_serializer(*args, **kwargs)

    def get_allowed_fields(self):
        return ['username']  # Specify the fields allowed to be updated

    def get_serializer_kwargs(self):
        kwargs = super().get_serializer_kwargs()
        kwargs['allowed_fields'] = self.get_allowed_fields()
        return kwargs


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


# class UserList(APIView):
#
#     def post(self, request):
#         # This api is to provide the list of matched students based on profile
#         # It should also provide the filters
#         pass
#
#
# class SyncContacts(APIView):
#
#     def post(self, request):
#         # This api is to sync contacts from outlook
#         pass