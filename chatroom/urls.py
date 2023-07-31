from django.urls import path

from .views import GetChanelId, GetMessagesList


urlpatterns = [
    path('get_channel_id/', GetChanelId.as_view(), name='get_channel_id'),
    path('get_messages/<int:channel_id>/', GetMessagesList.as_view(), name="get_messages"),
]
