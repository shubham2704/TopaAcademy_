# Generated by Django 2.2.2 on 2019-08-24 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_main', '0002_auto_20190823_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='test_id',
            field=models.IntegerField(),
        ),
    ]
