from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import  APIView

from universities.models import University
from .serializers import CommunitySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class Community(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Items per page')
        ]
    )
    def get(self, request, university_id):
        try:
            university = University.objects.get(id=university_id)
        except University.DoesNotExist:
            return Response({"error": "University does not exist"})
        serializer = CommunitySerializer(instance=university, context={'request':request})
        return Response(serializer.data)
