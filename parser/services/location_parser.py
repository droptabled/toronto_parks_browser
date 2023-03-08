from parser.models import Location, District, Facility, LocationTierFacility, TierFacility
import requests
import re
from bs4 import BeautifulSoup

class LocationParser:
    """Parsing info for a specific location"""

    def __init__(self, url):
        self.main_page = BeautifulSoup(requests.get(url).text, 'html.parser')

        partial = re.search("complex/\d+/", url)[0]
        park_id = re.search("\d+", partial)[0]
        try:
            self.location = Location.objects.get(park_id = park_id)
        except Location.DoesNotExist:
            self.location = Location(park_id = park_id)

    def parse_location(self):
        header = self.main_page.find("div", class_="accbox")
        self.location.name = header.find("h1").text.strip()

        address_bar = header.find("span", class_="addressbar")
        # Grab the first component of the header
        self.location.address = address_bar.find("span", class_="badge").contents[0].strip()
        
        district_text = address_bar.find("span", class_="addressbar").text.strip()
        district, _ = District.objects.get_or_create(name=district_text)
        self.location.district = district

        self.location.save()
        self.parse_location_facilities()

    def parse_location_facilities(self):
        self.location.location_tier_facilities.all().delete()

        facilities_tab = self.main_page.find("div", id="pfrComplexTabs-facilities")
        facility_rows = facilities_tab.select("tbody > tr")
        for facility_row in facility_rows:
            name, quantity_text, tier_text = [node.text for node in facility_row.children]
            quantity_arr = [int(str) for str in quantity_text.split("<br>")]
            tier_arr = tier_text.split("<br>")
            facility, _ = Facility.objects.get_or_create(name=name)

            for quantity, tier in zip(quantity_arr, tier_arr):
                tier_facility, _ = TierFacility.objects.get_or_create(facility=facility, tier=tier)
                LocationTierFacility(location=self.location, tier_facility=tier_facility, quantity=quantity).save()
        self.location.save()

