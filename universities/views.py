from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from rest_framework import generics, permissions
from rest_framework import filters
from .models import University, Program, Intake
from .serializers import UniversityListSerializer, ProgramSerializer, IntakeSerializer


# 1. API to list all the universities
class UniversityListAPIView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']


# 2. API to list the programs available in the university
class ProgramListAPIView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        university_id = self.kwargs['university_id']
        queryset = Program.objects.filter(university_id=university_id)
        return queryset


# 3. API to list the available Intakes in  the Program
class IntakeListAPIView(generics.ListAPIView):
    serializer_class = IntakeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['intake_name']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        program_id = self.kwargs['program_id']
        queryset = Intake.objects.filter(program_id=program_id)
        return queryset

