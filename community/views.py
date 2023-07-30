from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import  APIView

from universities.models import University
from .serializers import CommunitySerializer



# Create your views here.

class Community(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, university_id):
        try:
            university = University.objects.get(id=university_id)
        except University.DoesNotExist:
            return Response({"error": "University does not exist"})
        serializer = CommunitySerializer(instance=university, context={'request':request})
        return Response(serializer.data)
