from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Message
from .serializers import  MessageSerializer


class GetChanelId(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="API to get channel Id for personal chats",
                         manual_parameters = [
                             openapi.Parameter('id1', openapi.IN_QUERY, description="ID of user 1", type=openapi.TYPE_INTEGER),
                             openapi.Parameter('id2', openapi.IN_QUERY, description="ID of user 2", type=openapi.TYPE_INTEGER),
                         ]
                         )
    def get(self, request):
        id1 = request.GET.get("id1", None)
        id2 = request.GET.get("id2", None)
        if not id1 or not id2:
            return Response({"error": "id1 and id2 has to be passed as a part of the query params"},
                            status=status.HTTP_400_BAD_REQUEST)
        id1 = int(id1)
        id2 = int(id2)
        ids = [id1, id2]
        ids = sorted(ids)
        cid = (1 / 2) * (ids[0] + ids[1]) * (ids[0] + ids[1] + 1) + ids[1]
        cid = 1000000 + cid
        return Response({'channel_id': cid})



class GetMessagesList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, channel_id):
        messages = Message.objects.filter(channel_id=channel_id).order_by('-ctime')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
