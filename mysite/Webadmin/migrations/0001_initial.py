# Generated by Django 5.0.6 on 2024-07-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('specialized', models.TextField()),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
