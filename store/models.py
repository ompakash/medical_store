from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# MODEL FOR PATIENT
class Patient(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    user = models.OneToOneField(User(), on_delete=models.CASCADE,null=False)
    image = models.URLField()
    address = models.CharField(max_length=300,null=False)
    city = models.CharField(max_length=300,null=False)
    state = models.CharField(max_length=300,null=False)
    pincode = models.IntegerField(null=False)

    def __str__(self):
        return self.user.username



# MODEL FOR DOCTOR
class Doctor(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=False)
    image = models.URLField()
    address = models.CharField(max_length=300,null=False)
    city = models.CharField(max_length=300,null=False)
    state = models.CharField(max_length=300,null=False)
    pincode = models.IntegerField(null=False)

    def __str__(self):
        return self.user.username