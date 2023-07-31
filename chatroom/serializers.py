from rest_framework import serializers
from .models import Message
from community.serializers import ProfileSerializer


class MessageSerializer(serializers.ModelSerializer):
    sent_by = ProfileSerializer()
    ctime = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_ctime(self, post):
        formatted_date = post.ctime.strftime('%d %B %Y')
        formatted_time = post.ctime.strftime('%I:%M %p')
        return {'date': formatted_date, 'time': formatted_time}
