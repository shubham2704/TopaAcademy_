# Generated by Django 2.2.2 on 2019-07-11 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_auto_20190711_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branchs',
            old_name='branch_id',
            new_name='degree_id',
        ),
    ]