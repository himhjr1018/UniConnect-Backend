from django.db import models
from django.contrib.auth.models import User
from universities.models import Intake
from rest_framework.authtoken.models import Token


# Create your models here.
class CustomToken(Token):
    user = models.ForeignKey(User, related_name='custom_tokens', on_delete=models.CASCADE)


class UserProfile(User):
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.username + ":" + self.email


class Education(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    field_of_study = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.institution + ":" + self.degree


class Experience(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.company + ":" +  self.title


class InterestedProgram(models.Model):
    INTERESTED = 'Interested'
    APPLIED = 'Applied'
    ADMITTED = 'Admitted'
    JOINED = 'Joined'
    STAGE_CHOICES = [
        (INTERESTED, 'Interested'),
        (APPLIED, 'Applied'),
        (ADMITTED, 'Admitted'),
        (JOINED, 'Joined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intake = models.ForeignKey(Intake, on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)

    def __str__(self):
        return f'{self.user.username}  {self.program.name}'

