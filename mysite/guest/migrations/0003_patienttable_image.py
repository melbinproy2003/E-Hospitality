# Generated by Django 5.0.6 on 2024-07-07 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0002_alter_patienttable_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='patienttable',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
