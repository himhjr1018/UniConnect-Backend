from django.db import models

# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Intake(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    intake_name = models.CharField(max_length=100)

    def __str__(self):
        return self.prgram.university.name + self.program.name + self.intake_name

