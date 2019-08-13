from django.db import models

# Create your models here.

class student_latest_activity(models.Model):

    student_email = models.CharField(max_length=75)
    student_activity_json = models.TextField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default="")
    activity_name = models.CharField(max_length=250)
    current_session = models.CharField(max_length=100)

class student_rank(models.Model):

    student_email = models.CharField(max_length=75)
    rank_json = models.TextField()
    current_session = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default="")
    activity_name = models.CharField(max_length=250)