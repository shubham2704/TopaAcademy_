from django.db import models

# Create your models here.
class active(models.Model):
    added_by = models.CharField(max_length=75)
    status = models.CharField(max_length=75)
    announcement_type = models.CharField(max_length=100)
    send_to_group = models.CharField(max_length=100)
    sendto_ids_json = models.TextField()
    attachment_file = models.CharField(max_length=100)
    title = models.CharField(max_length=75)
    description = models.CharField(max_length=250)
    ischedule = models.BooleanField()
    schedule_date = models.DateField()
    date =  models.DateField()
