from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from universities.models import University
from users.models import UserProfile
from .models import Message, Channel
from .serializers import MessageSerializer, ChannelSerializer


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

    def get(self, request, channel_name):
        try:
            channel = Channel.objects.get(name=channel_name)
        except Channel.DoesNotExist:
            if 'uni' in channel_name:
                uniID = channel_name[4:]
                university = University.objects.get(id=uniID)
                channel = Channel(name=channel_name,type='university',university=university)
                channel.save()
            elif 'pvt' in channel_name:
                ls = channel_name.split("_")[1:]
                ls = [eval(i) for i in ls]
                userList = UserProfile.objects.filter(id__in=ls)
                channel = Channel(name=channel_name,type='private')
                channel.save()
                channel.users.set(userList)
            else:
                return Response({"error": "Channel Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            is_joined=True
            try:
                channel.users.get(id=request.user.id);
                print("User Joined")
            except:
                is_joined=False
                print("User Not Joined")
            messages = Message.objects.filter(channel=channel).order_by("-ctime")[:25]
            serializer = MessageSerializer(messages, many=True)
            currentUser = UserProfile.objects.get(id=request.user.id)
            #From channel.users, I need to remove the currentUser object and send it. If its not possible, easily. Just ping me tomorrow and I should be able to handle in the front end
            channelSerializer = ChannelSerializer(channel, context={'request': request})
            return Response({"id":channel.id,"is_joined":is_joined,"messages":serializer.data,"channel":channelSerializer.data})

