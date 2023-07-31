from django.db import models
from users.models import UserProfile


class Message(models.Model):
    content = models.TextField()
    sent_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    channel_id = models.BigIntegerField()
    ctime = models.DateTimeField(auto_now_add=True)
