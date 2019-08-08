from django.db import models

# Create your models here.

class details(models.Model):
    current_session = models.BooleanField()
    session_from = models.DateField()
    session_to = models.DateField()
    status = models.CharField(max_length=75)


class data(models.Model):
    session_id = models.ForeignKey(details, on_delete=models.CASCADE)
    data_status = models.BooleanField()
    program = models.CharField(max_length=100)
    option_txt = models.TextField()
    branch = models.CharField(max_length=100)

class data_semseter(models.Model):
    data_id = models.ForeignKey(data, on_delete=models.CASCADE)
    session_id = models.ForeignKey(details, on_delete=models.CASCADE)
    data_status = models.BooleanField()
    duration_type = models.CharField(max_length=100)
    duration_number = models.CharField(max_length=100)
    ClassTeacher_ID = models.CharField(max_length=100)
    option_txt = models.TextField()
    HOD_ID = models.CharField(max_length=100)

class academic_year(models.Model):
    session_id = models.ForeignKey(details, on_delete=models.CASCADE)
    status = models.BooleanField()
    from_ay = models.CharField(max_length=100)
    to_ay = models.CharField(max_length=100)
    label = models.CharField(max_length=500)


