# Generated by Django 4.1.4 on 2023-02-12 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0005_programcategory_rename_address1_location_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='park_id',
            field=models.IntegerField(unique=True),
        ),
    ]
