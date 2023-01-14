from django.core.management.base import BaseCommand, CommandError
from parser.models import Facility, FacilityTier
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = "parses the data for facility types and tiers"

    def handle(self, *args, **options):
        base_url = "https://www.toronto.ca"
        url = "https://www.toronto.ca/data/parks/prd/facilities/ratings/index.html"
        main_page = BeautifulSoup(requests.get(url).text, 'html.parser')
        facility_node = main_page.find("div", id="infobox")

        facility_count = 0
        facility_tier_count = 0
        for node in facility_node("div", recursive=False):
            facility, _ = Facility.objects.get_or_create(slug=node['id'])
            facility_count += 1
            facility.name = node.find("h2").text
            img = node.find("img")
            facility.image_url = base_url + img['src']
            facility.alt_text = img['alt']
            facility.save()

            facility.tiers.all().delete()
            tier_div = node.find("div", class_="ratingdata")
            for tier in tier_div("h3", recursive=False):
                FacilityTier.objects.get_or_create(facility=facility, tier=tier.text)
                facility_tier_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully parsed {facility_count} facilites and {facility_tier_count} tiers'))