# Generated by Django 2.2.2 on 2019-08-14 08:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('view_test_info', '0002_start_test_details_test_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='start_test_details',
            name='test_started',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
