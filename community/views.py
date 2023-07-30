from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from universities.models import University
from users.models import UserProfile
from .models import Post
from .serializers import CommunitySerializer, AddPostSerializer, PostSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class Community(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Items per page'),
            openapi.Parameter('tag', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Tag to filter posts', explode=True)
        ]
    )
    def get(self, request, university_id):
        try:
            university = University.objects.get(id=university_id)
        except University.DoesNotExist:
            return Response({"error": "University does not exist"})
        serializer = CommunitySerializer(instance=university, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AddPostSerializer)
    def post(self, request, university_id):
        try:
            university = University.objects.get(id=university_id)
        except University.DoesNotExist:
            return Response({"error": "University does not exist"})

        serializer = AddPostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post()
            post.content = serializer.validated_data["content"]
            post.tags = serializer.validated_data["tags"]
            profile = UserProfile.objects.get(id=request.user.id)
            post.posted_by = profile
            post.university = university
            post.save()
            serializer = PostSerializer(instance=post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

