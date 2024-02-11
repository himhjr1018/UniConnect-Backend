from django.db import models
from universities.models import University, Intake
from users.models import User, UserProfile


# Create your models here.
class Post(models.Model):
    university = models.ForeignKey(University, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    liked_by = models.ManyToManyField(UserProfile)
    tags = models.TextField()
    posted_by = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField()
    posted_by = models.ForeignKey(UserProfile, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
