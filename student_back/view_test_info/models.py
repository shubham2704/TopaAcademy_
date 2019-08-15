from django.db import models

# Create your models here.


class start_test_details(models.Model):
    
    test_session_id = models.CharField(max_length=250)
    test_useremail = models.CharField(max_length=250)
    test_istimer = models.BooleanField()
    timer_duration = models.CharField(max_length=20)
    test_started = models.DateTimeField(auto_now_add=True)
    test_settings = models.TextField(default="")
    scored = models.CharField(max_length=20)
    total_score = models.CharField(max_length=20)
    TestType = models.CharField(max_length=20)
    TestID = models.CharField(max_length=20)
    resumeable = models.BooleanField()
    TestStarted = models.BooleanField()
    TestStatus = models.CharField(max_length=20, default="Started")

class submited_test_report(models.Model):
    
    test_session_id = models.CharField(max_length=250)
    test_useremail = models.CharField(max_length=250)
    test_started = models.DateTimeField()
    test_submited = models.DateTimeField(auto_now_add=True)
    submited_det = models.TextField()
    scored = models.CharField(max_length=20, default="")
    total_score = models.CharField(max_length=20, default="")
    correct = models.CharField(max_length=20)
    wrong = models.CharField(max_length=20)
    clg_rnk = models.CharField(max_length=20, default="")
    class_rnk = models.CharField(max_length=20, default="")
    TestStatus = models.CharField(max_length=20, default="Submited")
