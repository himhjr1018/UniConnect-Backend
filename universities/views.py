from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework import filters
from .models import University, Program, Intake
from .serializers import UniversityListSerializer, ProgramSerializer, IntakeSerializer, UniversityAddSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

# 1. API to list all the universities
class UniversityListAPIView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    filterset_fields = ['country']




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


class CountryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        countries = University.objects.order_by('country').values_list('country', flat=True).distinct()
        clist = [{'value': country, 'label':country} for country in countries]
        return Response(clist)


class UniversityListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='country',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter universities by country (case-sensitive)',
            ),
        ],
        responses={200: UniversityListSerializer(many=True)},
    )
    def get(self, request, format=None):
        country = request.GET.get('country', None)
        if country:
            universities = University.objects.filter(country=country).order_by('name')
        else:
            return Response(status=400)
        universities = universities.values_list('id', 'name')
        uni_list = [{'value': id, 'label': name} for id, name in universities]
        return Response(uni_list)


class UniversityCreateView(APIView):

    @swagger_auto_schema(request_body=UniversityAddSerializer)
    def post(self, request, format=None):
        serializer = UniversityAddSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

