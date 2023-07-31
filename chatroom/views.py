from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.models import UserProfile
from .models import Message, Channel
from .serializers import  MessageSerializer


class JoinChannel(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            return Response({"error": "Channel Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.get(id=request.user.id)

        channel.users.add(user_profile)
        return Response(status=status.HTTP_201_CREATED)


class GetMessagesList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            return Response({"error": "Channel Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.filter(channel=channel).order_by("-ctime")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)




