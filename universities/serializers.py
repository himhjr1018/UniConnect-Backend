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