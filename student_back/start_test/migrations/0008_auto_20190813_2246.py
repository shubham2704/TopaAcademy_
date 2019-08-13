# Generated by Django 2.2.2 on 2019-08-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start_test', '0007_remove_details_test_istimer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='details',
            name='TestID',
        ),
        migrations.AddField(
            model_name='details',
            name='resumeable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='details',
            name='test_istimer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='details',
            name='TestType',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='details',
            name='scored',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='details',
            name='test_session_id',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='details',
            name='test_useremail',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='details',
            name='timer_duration',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='details',
            name='total_score',
            field=models.CharField(max_length=20),
        ),
    ]
