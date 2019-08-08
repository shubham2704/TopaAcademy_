from django.db import models

# Create your models here.

class Steam(models.Model):

    steam_name = models.CharField(max_length=75)
    steam_link_id = models.IntegerField()
    steam_status = models.CharField(max_length=25)
    date = models.DateField(auto_now_add=True)

class Steam_Data(models.Model):
    
    steam_id = models.IntegerField()
    steam_data_json = models.TextField()
    multilevel_data = models.CharField(max_length=25)
    steam_status = models.CharField(max_length=25)
    date = models.DateField(auto_now_add=True)


