from rest_framework import serializers
from users.models import UserProfile, Education, Experience, InterestedProgram
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


class AddEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('profile', )


class AddExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ('profile', )


class AddInterestedProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedProgram
        fields = ['intake', 'stage']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['profile', ]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ['profile', ]


class InterestedProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedProgram
        fields = ['intake', 'stage']


class UploadProfilePicSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class EditIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'city', 'state', 'country']


class UpdateUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']

    def __init__(self, *args, **kwargs):
        allowed_fields = kwargs.pop('allowed_fields', None)
        super().__init__(*args, **kwargs)
        if allowed_fields:
            self.fields = {field: self.fields[field] for field in allowed_fields}


class EducationDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree', 'institution', 'city', 'state', 'country', 'start_date', 'end_date', 'field_of_study']


class ExperienceDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'title', 'company', 'city', 'state', 'country', 'start_date', 'end_date', 'description']


class InterestedProgramDSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedProgram
        fields = ['id', 'intake', 'stage']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    educations = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    interested_programs = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country',
                  'profile_picture', 'educations', 'experiences', 'interested_programs', 'con_connected']

    def get_educations(self, obj):
        educations = Education.objects.filter(profile=obj)
        serializer = EducationDSerializer(educations, many=True)
        return serializer.data

    def get_experiences(self, obj):
        educations = Experience.objects.filter(profile=obj)
        serializer = ExperienceDSerializer(educations, many=True)
        return serializer.data

    def get_interested_programs(self, obj):
        ips = InterestedProgram.objects.filter(profile=obj)
        serializer = InterestedProgramDSerializer(ips, many=True)
        return serializer.data