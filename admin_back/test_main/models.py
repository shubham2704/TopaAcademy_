from django.db import models

# Create your models here.

class question(models.Model):
    test_id = models.IntegerField()
    question  = models.TextField()
    explanation = models.TextField()
    a1 = models.BooleanField(default=False)
    a2 = models.BooleanField(default=False)
    a3 = models.BooleanField(default=False)
    a4 = models.BooleanField(default=False)
    o1 = models.CharField(max_length=150)
    o2 = models.CharField(max_length=150)
    o3 = models.CharField(max_length=150)
    o4 = models.CharField(max_length=150)