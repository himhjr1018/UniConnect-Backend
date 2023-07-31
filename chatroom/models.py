from django.db import models
from users.models import UserProfile


TYPE_CHOICES  = [
    ('private', 'private'),
    ("university", "university"),
    ("intake", "intake")
]


class Channel(models.Model):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(UserProfile)
    type = models.CharField(max_length=256, choices=TYPE_CHOICES)


class Message(models.Model):
    content = models.TextField()
    sent_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
