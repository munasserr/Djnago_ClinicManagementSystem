from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

USER_STATUS = (('Doctor', 'Doctor'), ('Reception', 'Reception'))



class Patient(models.Model):
    name = models.CharField(max_length=100,blank=False, null=False)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    bloodgroup = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=False)
    age = models.IntegerField(blank=False, null=True)
    notes = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add =True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return str(self.name)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient,null=True,on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False,)
    time = models.TimeField(null=False, blank=False)
    status = models.CharField(max_length=10, blank=True, null=True,default="لم يتم")
    notes = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} (حجز {self.id}) "
    class Meta:
        ordering  = ('date',)


class Bill(models.Model):
    date = models.DateField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment ,null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField(blank=False, null=True)
    notes = models.TextField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.date}"
    
    
    
class UserCustom(AbstractUser):
    status = models.CharField(max_length=10, choices=USER_STATUS)

    