from django.db import models

# Create your models here.


class start_test_details(models.Model):
    
    test_session_id = models.CharField(max_length=250)
    test_useremail = models.CharField(max_length=250)
    test_istimer = models.BooleanField()
    timer_duration = models.CharField(max_length=20)
    scored = models.CharField(max_length=20)
    total_score = models.CharField(max_length=20)
    TestType = models.CharField(max_length=20)
    TestID = models.CharField(max_length=20)
    resumeable = models.BooleanField()
    TestStarted = models.BooleanField()
