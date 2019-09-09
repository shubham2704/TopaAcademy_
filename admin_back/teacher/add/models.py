from django.db import models

# Create your models here.
class add(models.Model):
    prefix = models.CharField(max_length=10)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    desination = models.CharField(max_length=75)
    department = models.CharField(max_length=75)
    epployee_id = models.CharField(max_length=75)
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=75)
    phone = models.CharField(max_length=75)
    avatar = models.ImageField(max_length=100,default="/static/teacher/assets/img/avatar.png")
    password = models.CharField(max_length=250)
