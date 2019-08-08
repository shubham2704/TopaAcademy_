# Generated by Django 2.2.2 on 2019-08-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_by', models.CharField(max_length=75)),
                ('status', models.CharField(max_length=75)),
                ('title', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('categoryOne', models.CharField(max_length=250)),
                ('categoryTwo', models.CharField(max_length=250)),
                ('categoryThree', models.CharField(max_length=250)),
                ('categoryFour', models.CharField(max_length=250)),
                ('isSCP', models.BooleanField()),
                ('SCP_program', models.CharField(max_length=100)),
                ('SCP_branch', models.CharField(max_length=100)),
                ('SCP_semester', models.CharField(max_length=100)),
            ],
        ),
    ]
