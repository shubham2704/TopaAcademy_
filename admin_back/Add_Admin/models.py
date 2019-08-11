from django.db import models

# Create your models here.

class users(models.Model):

    first_name = models.CharField(max_length=75)
    staff_id = models.CharField(max_length=75, default="")
    lastname = models.CharField(max_length=75)
    employe_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    email = models.CharField(max_length=75)
    role = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=25)
    added_by_user = models.CharField(max_length=75,default='')
    password = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

class activity(models.Model):
    
    admin_email = models.CharField(max_length=75)
    activity_name = models.CharField(max_length=75)
    activity_des = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)    

