# Generated by Django 4.1.4 on 2023-01-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_facility_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitytier',
            name='tier',
            field=models.CharField(max_length=10),
        ),
    ]
