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
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)
    image = models.URLField()
    address = models.CharField(max_length=300,null=False)
    city = models.CharField(max_length=300,null=False)
    state = models.CharField(max_length=300,null=False)
    pincode = models.IntegerField(null=False)

    def __str__(self):
        return self.user.username

# MODEL FOR BLOGPOST

class Blogpost(models.Model):
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.URLField()
    category = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    content = models.CharField(max_length=5000)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
#Appointment class
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    required_speciality = models.CharField(max_length=500)
    datetime_of_appointment = models.DateTimeField(auto_now=False,auto_now_add=False)
    # start_time = models.TimeField(auto_now=False,auto_now_add=False)

    def __str__(self):
        return self.doctor.user.first_name