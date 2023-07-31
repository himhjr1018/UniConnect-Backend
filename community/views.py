from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from universities.models import University
from users.models import UserProfile
from .models import Post, Comment
from .serializers import CommunitySerializer, AddPostSerializer, PostSerializer, AddCommentSerializer, CommentSerializer
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


class LikePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Likes Post or Unlikes Post depends on current status")
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error':"Post Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        profile = UserProfile.objects.get(id=request.user.id)
        if profile in post.liked_by.all():
            post.liked_by.remove(profile)
        else:
            post.liked_by.add(profile)

        serializer = PostSerializer(instance=post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="get all the comments of a post")
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': "Post Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(post.comments.all().order_by("-ctime"), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AddCommentSerializer)
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error':"Post Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = Comment()
            comment.content = serializer.validated_data["content"]
            profile = UserProfile.objects.get(id=request.user.id)
            comment.posted_by = profile
            comment.post = post
            comment.save()
            serializer  =CommentSerializer(instance=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': "Comment DoesNot Exist"}, status=status.HTTP_404_NOT_FOUND)
        print(comment.posted_by.id)
        print(request.user.id)
        if comment.posted_by.id != request.user.id:
            return Response({'error': "You are not authorised delete this comment"}, status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': "Post DoesNot Exist"}, status=status.HTTP_404_NOT_FOUND)

        if post.posted_by.id != request.user.id:
            return Response({'error': "You are not authorised delete this post"}, status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

