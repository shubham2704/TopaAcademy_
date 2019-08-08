from django.db import models

# Create your models here.

class branch_degree(models.Model):

    degree_name = models.CharField(max_length=75)
    degree_status = models.CharField(max_length=25)
    date = models.DateField(auto_now_add=True)
    program = models.CharField(max_length=100, default="")
    duration = models.CharField(max_length=100, default="")
    semester = models.CharField(max_length=100, default="")

class branchs(models.Model):
    
    degree_id = models.IntegerField()
    degree_name = models.CharField(max_length=75, default="")
    branch_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    