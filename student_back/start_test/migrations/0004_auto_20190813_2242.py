# Generated by Django 2.2.2 on 2019-08-13 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start_test', '0003_auto_20190813_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='FirstOpen',
            field=models.BooleanField(),
        ),
    ]
