# Generated by Django 2.2.2 on 2019-08-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='a2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='a3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='a4',
            field=models.BooleanField(default=False),
        ),
    ]
