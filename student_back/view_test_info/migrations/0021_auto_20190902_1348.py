# Generated by Django 2.2.2 on 2019-09-02 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_test_info', '0020_submited_test_report_resultstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='submited_test_report',
            name='ExamID',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='submited_test_report',
            name='TestID',
            field=models.CharField(default='', max_length=20),
        ),
    ]
