from django.db import models


class test_details(models.Model):
    
    test_name = models.CharField(max_length=75)
    description  = models.CharField(max_length=150)
    isSCT_test = models.BooleanField()
    SCTSteam = models.CharField(max_length=150, default='')
    SCTBranch = models.CharField(max_length=150, default='')
    SCTSemester = models.CharField(max_length=150, default='')
    TestDifficulty = models.CharField(max_length=75)
    category_level = models.CharField(max_length=75)
    steam = models.CharField(max_length=25, default='')
    TestType = models.CharField(max_length=75, default='')
    AskQuestion = models.CharField(max_length=75, default='')
    category_one = models.CharField(max_length=75, default='')
    category_two = models.CharField(max_length=75,default='')
    category_three = models.CharField(max_length=500, default='')
    status = models.CharField(max_length=50, default='Created')
    added_by = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)


class test_details_advanced(models.Model):
    
    test_id = models.CharField(max_length=75)
    isTimer  = models.BooleanField()
    TimerLength = models.CharField(max_length=50, default='0')
    isAvailDuration = models.BooleanField()
    DurationFrom = models.CharField(max_length=75, default='0')
    DurationTo = models.CharField(max_length=25, default='0')
    sendNotification = models.CharField(max_length=25, default='')
    NotificationSettings = models.CharField(max_length=25,default='Dont Send')
    date = models.DateField(auto_now_add=True)


class test_data(models.Model):
    
    test_id = models.IntegerField(default=0)
    question  = models.TextField()
    optionOne = models.CharField(max_length=150)
    optionTwo = models.CharField(max_length=150)
    optionThree = models.CharField(max_length=150)
    optionFour = models.CharField(max_length=150, default="")
    answer = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)

