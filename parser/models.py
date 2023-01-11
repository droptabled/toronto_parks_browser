from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100)

class Facility(models.Model):
    name = models.CharField(max_length=100)

class FacilityTier(models.Model):
    tier = models.CharField(
        max_length=1,
        choices=[
            ('P', 'Premier'),
            ('A', 'A'),
            ('B','B'),
            ('C', 'C')
        ]
    )
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="tiers")
    features = models.TextField()

class Location(models.Model):
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    facilities = models.ManyToManyField(Facility, through='LocationFacilities', related_name="locations")

class LocationFacilities(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location_facilities")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="location_facilities")
    count = models.PositiveIntegerField()
    extra_description = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'facility'], name='no_duplicate_facility_at_location'),
        ]

