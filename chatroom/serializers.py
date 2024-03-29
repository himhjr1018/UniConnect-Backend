from rest_framework import serializers
from .models import Message, Channel
from community.serializers import ProfileSerializer


class MessageSerializer(serializers.ModelSerializer):
    sent_by = ProfileSerializer()
    ctime = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id","content","sent_by","ctime"]

    def get_ctime(self, post):
        formatted_date = post.ctime.strftime('%d %B %Y')
        formatted_time = post.ctime.strftime('%I:%M %p')
        return {'date': formatted_date, 'time': formatted_time}


class ChannelSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ["id","name","type","users"]

    def get_users(self, channel):
        request = self.context.get("request")
        users = channel.users.exclude(id=request.user.id)
        p_serializer = ProfileSerializer(users, many=True)
        return p_serializer.data

