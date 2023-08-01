from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from universities.models import Intake, Program
from users.models import CustomToken, Education, Experience, InterestedProgram
from django.contrib.auth.models import User

from users.serializers import LoginSerializer, SignupSerializer, AddEducationSerializer, AddExperienceSerializer, \
    AddInterestedProgramSerializer, EducationSerializer, ExperienceSerializer, InterestedProgramSerializer, \
    UploadProfilePicSerializer, EditIntroSerializer, UpdateUserNameSerializer, UserProfileDetailSerializer, \
    AddFavSerializer
from rest_framework import status, generics, permissions
import random
import string
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfile
from rest_framework.parsers import MultiPartParser
from django.http import Http404
from django.db.models import Q
import requests
from django.utils import timezone
from microsoft_graph.utils import graph_call, refresh_access_token, OUTLOOK_CONTACTS_API
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


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
        try:

            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user_profile = UserProfile(**serializer.validated_data)
                user_profile.username = generate_username(user_profile.first_name)
                user_profile.set_password(serializer.validated_data['password'])
                user_profile.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            raise e


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

    def get_serializer_context(self):
        context = super(UserProfileDetailAPIView, self).get_serializer_context()
        context['request'] = self.request
        return context

class OUserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile_id = self.kwargs["id"]  # Assuming the URL parameter is named "profile_id"
        try:
            return UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            raise Http404("Profile Not Found")

    def get_serializer_context(self):
        context = super(UserProfileDetailAPIView, self).get_serializer_context()
        context['request'] = self.request
        return context



def get_filter_by_contacts(queryset, profile):
    if not profile.con_connected:
        return queryset

    refresh_access_token(profile)
    resp = graph_call(OUTLOOK_CONTACTS_API, profile.con_access_token, method="GET")
    resp = resp.json()
    value = resp['value']
    mobile_numbers = []
    for i in value:
        if i["mobilePhone"]:
            mobile_numbers.append(i["mobilePhone"])
    return queryset.filter(phone_number__in=mobile_numbers)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('filter_by_contacts', openapi.IN_QUERY, description='Filter by contacts',
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('filter_by_ip', openapi.IN_QUERY, description='Filter by IP', type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description='Search query', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(education__institution__icontains=search_query) |
                Q(experience__company__icontains=search_query)
            )

        filter_by_contacts = self.request.query_params.get('filter_by_contacts', None)
        filter_by_ip = self.request.query_params.get('filter_by_ip', None)
        profile = UserProfile.objects.get(id=self.request.user.id)

        if filter_by_contacts == "true":
            queryset = get_filter_by_contacts(queryset, profile)

        if filter_by_ip == "true":
            interested_programs = profile.interestedprogram_set.all()
            intakes = interested_programs.values_list('intake', flat=True).distinct()
            queryset = queryset.filter(interestedprogram__intake__in=intakes)
        queryset = queryset.exclude(id=profile.id).distinct()
        print(queryset.count())
        serializer = self.get_serializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)


class InterestedProgramAPIView(APIView):
    def get(self, request, user_id):
        user = request.user  # Assuming the user is authenticated and you are using sessions

        interested_programs = InterestedProgram.objects.filter(profile__id=user_id)
        universities_data = []

        for interested_program in interested_programs:
            uni = interested_program.intake.program.university
            program = interested_program.intake.program

            # Check if the university is already in the universities_data list
            uni_data = next((item for item in universities_data if item['id'] == uni.id), None)

            if not uni_data:
                # Create a new university entry in the universities_data list
                uni_data = {
                    'name': uni.name,
                    'id': uni.id,
                    'programs': [],
                }
                universities_data.append(uni_data)

            # Check if the program is already in the programs list of the university entry
            program_data = next((item for item in uni_data['programs'] if item['name'] == program.name), None)

            if not program_data:
                # Create a new program entry in the programs list of the university entry
                program_data = {
                    'name': program.name,
                    'id': program.id,
                    'intakes': [],
                }
                uni_data['programs'].append(program_data)

            # Add the intake to the intakes list of the program entry
            program_data['intakes'].append({'id': interested_program.intake.id, 'name': interested_program.intake.intake_name, \
                                            'stage': interested_program.stage})

        return Response(universities_data)


class InterestedProgramView(APIView):

    @swagger_auto_schema(request_body=AddFavSerializer)
    def post(self, request):
        data = request.data

        try:
            program = Program.objects.get(id=data["program_id"])
        except Program.DoesNotExist:
            return Response({"error": "Given Profile Doesnot Exists"}, status=status.HTTP_404_NOT_FOUND)

        stage = data.get("stage", "Interested")

        intake, created = Intake.objects.get_or_create(intake_name=data["intake_name"], program=program)
        profile = UserProfile.objects.get(id=request.user.id)
        ip, created = InterestedProgram.objects.get_or_create(profile=profile, intake=intake)
        if not created:
            return Response({"error": "This program is already is in your favourites"})
        ip.stage = stage
        ip.save()
        return Response(status=status.HTTP_200_OK)

