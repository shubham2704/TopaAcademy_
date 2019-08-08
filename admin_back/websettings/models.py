from django.db import models

# Create your models here.

class settings(models.Model):

    website_name = models.CharField(max_length=75)
    website_description = models.CharField(max_length=250)
    timezone = models.CharField(max_length=25)
    salt = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='logo/')
    favicon = models.ImageField(upload_to='favicon/')
    student_signup = models.CharField(max_length=10)
    sms_notification = models.CharField(max_length=250)
    email_notification = models.CharField(max_length=10)
    smtp_host = models.CharField(max_length=75)
    smtp_port = models.IntegerField()
    smtp_email = models.CharField(max_length=75)
    smtp_username = models.CharField(max_length=75)
    smtp_password = models.CharField(max_length=75)
    date = models.DateTimeField(auto_now_add=True)




