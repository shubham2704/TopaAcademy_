# Generated by Django 2.2.2 on 2019-07-08 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Add_Admin', '0002_auto_20190708_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='department',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='users',
            name='employe_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
