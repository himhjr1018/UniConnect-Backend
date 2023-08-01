from django.urls import path

from .views import JoinChannel, GetMessagesList


urlpatterns = [
    path('join/<int:channel_id>/', JoinChannel.as_view(), name='join_channel'),
    path('<slug:channel_name>/messages/', GetMessagesList.as_view(), name='messages'),
]
