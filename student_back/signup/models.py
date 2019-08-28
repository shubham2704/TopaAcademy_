from django.db import models

# Create your models here.

class student_user(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    avatar = models.ImageField()
    email = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    otp = models.CharField(max_length=10, default="")
    password = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    account_status = models.CharField(max_length=75)
    email_hash = models.CharField(max_length=100)
    phone_status = models.CharField(max_length=25)
    date_of_birth = models.CharField(max_length=25, default="")
    email_status = models.CharField(max_length=25)


class student_academic(models.Model):
    student_id = models.ForeignKey(student_user, on_delete=models.CASCADE)
    branch = models.CharField(max_length=75)
    student_email = models.CharField(max_length=75, default="")
    semester = models.IntegerField()
    batch = models.CharField(max_length=75)
    profile = models.ImageField(default='')
    date = models.DateField(auto_now_add=True)
    subject_preference = models.TextField()
    goal = models.CharField(max_length=75)
    EnrollNo = models.CharField(max_length=75, default="")
    ClgStatus = models.CharField(max_length=75, default="")
    
class student_dashboard_metrices(models.Model):
    student_id = models.ForeignKey(student_user, on_delete=models.CASCADE)
    college_level_rank = models.CharField(max_length=75)
    class_level_rank = models.CharField(max_length=75)
    student_email = models.CharField(max_length=75, default="")
    date = models.DateField(auto_now_add=True)

