from django.db import models

# Create your models here.

class content(models.Model):
    create_by = models.CharField(max_length=75)
    status = models.CharField(max_length=75)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    content = models.TextField()
    categoryOne = models.CharField(max_length=250)
    categoryTwo = models.CharField(max_length=250)
    categoryThree = models.CharField(max_length=250)
    categoryFour = models.CharField(max_length=250)
    isSCP = models.BooleanField()
    SCP_program = models.CharField(max_length=100)
    SCP_branch = models.CharField(max_length=100)
    SCP_semester = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    creation_session = models.CharField(max_length=75, default="")

class attachment(models.Model):
    status = models.CharField(max_length=75)
    creation_session = models.CharField(max_length=250)
    filename = models.CharField(max_length=250)
    upload = models.FileField(upload_to='upload_attachment/')
    actual_filename = models.CharField(max_length=250)
    extension = models.CharField(max_length=75)