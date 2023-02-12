from django.db import models
import constants

class District(models.Model):
    name = models.CharField(max_length=100)

class Facility(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255, null=True)
    alt_text = models.CharField(max_length=100, null=True)

    def page_link(self):
        return f"{constants.BASE_URL}/data/parks/prd/facilities/ratings/index.html#{self.slug}"

class FacilityTier(models.Model):
    tier = models.CharField(max_length=10)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="tiers")
    features = models.TextField()

class Location(models.Model):
    park_id = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
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

class ProgramCategory(models.Model):
    name = models.CharField(max_length=100)

class Program(models.Model):
    name = models.CharField(max_length=100)
    program_category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, related_name="programs")
    lower_age = models.IntegerField()
    upper_age = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_drop_in = models.BooleanField()
