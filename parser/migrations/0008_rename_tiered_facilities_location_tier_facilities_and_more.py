# Generated by Django 4.1.4 on 2023-03-08 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0007_locationtierfacility_remove_location_facilities_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='tiered_facilities',
            new_name='tier_facilities',
        ),
        migrations.RenameField(
            model_name='locationtierfacility',
            old_name='count',
            new_name='quantity',
        ),
    ]
