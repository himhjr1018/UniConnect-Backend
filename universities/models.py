from django.db import models

# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    domain = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.university.name + ":" + self.name


class Intake(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    intake_name = models.CharField(max_length=100)

    def __str__(self):
        return self.program.university.name + ": " +self.program.name + ": " + self.intake_name

