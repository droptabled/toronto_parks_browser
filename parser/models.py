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

class TierFacility(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="tiers")
    tier = models.CharField(max_length=10)
    features = models.TextField()

class Location(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    tier_facilities = models.ManyToManyField(TierFacility, through='LocationTierFacility', related_name="locations")
    park_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)

class LocationTierFacility(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location_tier_facilities")
    tier_facility = models.ForeignKey(TierFacility, on_delete=models.CASCADE, related_name="location_tier_facilities")
    quantity = models.PositiveIntegerField()
    extra_description = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'tier_facility'], name='no_duplicate_tier_facility_at_location'),
        ]

class ProgramCategory(models.Model):
    name = models.CharField(max_length=100)

class Program(models.Model):
    program_category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=100)
    is_drop_in = models.BooleanField()

class ProgramInstance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="program_instances")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="instances")
    lower_age = models.IntegerField()
    upper_age = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
