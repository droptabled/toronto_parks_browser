# Generated by Django 4.1.4 on 2023-01-14 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0003_alter_facilitytier_tier'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='alt_text',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='image_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
