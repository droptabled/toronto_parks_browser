# Generated by Django 4.1.4 on 2023-02-27 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0006_alter_location_park_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationTierFacility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('extra_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='facilities',
        ),
        migrations.RenameModel(
            old_name='FacilityTier',
            new_name='TierFacility',
        ),
        migrations.DeleteModel(
            name='LocationFacilities',
        ),
        migrations.AddField(
            model_name='locationtierfacility',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_tier_facilities', to='parser.location'),
        ),
        migrations.AddField(
            model_name='locationtierfacility',
            name='tier_facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_tier_facilities', to='parser.tierfacility'),
        ),
        migrations.AddField(
            model_name='location',
            name='tiered_facilities',
            field=models.ManyToManyField(related_name='locations', through='parser.LocationTierFacility', to='parser.tierfacility'),
        ),
        migrations.AddConstraint(
            model_name='locationtierfacility',
            constraint=models.UniqueConstraint(fields=('location', 'tier_facility'), name='no_duplicate_tier_facility_at_location'),
        ),
    ]
