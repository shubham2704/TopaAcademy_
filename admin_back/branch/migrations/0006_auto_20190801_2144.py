# Generated by Django 2.2.2 on 2019-08-01 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0005_auto_20190801_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchs',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='branchs',
            name='program',
        ),
        migrations.RemoveField(
            model_name='branchs',
            name='semester',
        ),
        migrations.AddField(
            model_name='branch_degree',
            name='duration',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='branch_degree',
            name='program',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='branch_degree',
            name='semester',
            field=models.CharField(default='', max_length=100),
        ),
    ]