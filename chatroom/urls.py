from django.urls import path

from .views import JoinChannel, GetMessagesList


urlpatterns = [
    path('join/<int:channel_id>/', JoinChannel.as_view(), name='join_channel'),
    path('<int:channel_id>/messages/', GetMessagesList.as_view(), name='messages'),

]
