# Generated by Django 2.2.2 on 2019-08-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.IntegerField(max_length=75)),
                ('question', models.TextField()),
                ('explanation', models.TextField()),
                ('a1', models.BooleanField(default=False)),
                ('o1', models.CharField(max_length=150)),
                ('o2', models.CharField(max_length=150)),
                ('o3', models.CharField(max_length=150)),
                ('o4', models.CharField(max_length=150)),
            ],
        ),
    ]
