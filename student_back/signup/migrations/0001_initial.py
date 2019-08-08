# Generated by Django 2.2.2 on 2019-07-10 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='student_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('avatar', models.ImageField(upload_to='')),
                ('email', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=500)),
                ('date', models.DateField(auto_now_add=True)),
                ('account_status', models.CharField(max_length=75)),
                ('email_hash', models.CharField(max_length=100)),
                ('phone_status', models.CharField(max_length=25)),
                ('email_status', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='student_dashboard_metrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_level_rank', models.CharField(max_length=75)),
                ('class_level_rank', models.CharField(max_length=75)),
                ('date', models.DateField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.student_user')),
            ],
        ),
        migrations.CreateModel(
            name='student_academic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField()),
                ('batch', models.CharField(max_length=75)),
                ('branch', models.CharField(max_length=75)),
                ('date', models.DateField(auto_now_add=True)),
                ('subject_preference', models.CharField(max_length=150)),
                ('goal', models.CharField(max_length=75)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.student_user')),
            ],
        ),
    ]
