# Generated by Django 4.1.4 on 2023-03-19 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0009_remove_program_date_remove_program_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='programinstance',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='program_instances', to='parser.location'),
            preserve_default=False,
        ),
    ]
