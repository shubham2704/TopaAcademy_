# Generated by Django 2.2.2 on 2019-08-11 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_Admin', '0004_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='staff_id',
            field=models.CharField(default='', max_length=75),
        ),
    ]
