from rest_framework import serializers

from .models import University, Program, Intake


class UniversityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name']


class IntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intake
        fields = ['id', 'intake_name']


class UniversityAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class ProgramAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class IPIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intake
        fields = ['intake_name']


class IPProgramSerializer(serializers.ModelSerializer):
    intakes = IPIntakeSerializer(many=True)

    class Meta:
        model = Program
        fields = ['program_name', 'intakes']


class IPUniversitySerializer(serializers.ModelSerializer):
    programs = IPProgramSerializer(many=True, source='program_set')

    class Meta:
        model = University
        fields = ['uni_name', 'id', 'programs']
