# Generated by Django 2.2.2 on 2019-08-01 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0006_auto_20190801_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchs',
            name='degree_name',
            field=models.CharField(default='', max_length=75),
        ),
    ]
