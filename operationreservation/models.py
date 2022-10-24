import imp
from django.db import models
from django.urls import reverse
from datetime import date, timedelta
# Create your models here.


class Operation(models.Model):
    #name = models.CharField(max_length=70)
    doctor_name = models.CharField(max_length=70, default='')
    patient_id = models.FloatField(default=0)
    date = models.DateField(default=date.today())
    duration = models.FloatField(default=0)
    emergency = models.FloatField(default=0)
    department_id = models.CharField(max_length=20, default='')
    room_id = models.CharField(max_length=10, default='')

    def get_success_url(self):
        return reverse('operationreservation:index')

    def __str__(self):
        return f"{self.id}, {self.doctor_name}, {self.patient_id}, {self.date}, {self.duration}, {self.emergency}, {self.department_id}, {self.room_id}"


class Department(models.Model):
    name = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    date = models.DateField()
    #operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.capacity})"


class OpRoom(models.Model):
    name = models.CharField(max_length=10)
    capacity = models.IntegerField(default=0)
    date = models.DateField()
    #operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.id}"
