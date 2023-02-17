from parser.models import Location, District
import requests
import re
from bs4 import BeautifulSoup

class LocationParser:
    """Parsing info for a specific location"""

    def __init__(self, url):
        self.url = url

        partial = re.search("complex/\d+/", url)[0]
        park_id = re.search("\d+", partial)[0]
        try:
            self.location, _ = Location.objects.get(park_id = park_id)
        except Location.DoesNotExist:
            self.location = Location(park_id = park_id)

    def parse_location(self):
        main_page = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        header = main_page.find("div", class_="accbox")
        self.location.name = header.find("h1").text.strip()

        address_bar = header.find("span", class_="addressbar")
        # Grab the first component of the header
        self.location.address = address_bar.find("span", class_="badge").contents[0].strip()
        
        district_text = address_bar.find("span", class_="addressbar").text.strip()
        district, _ = District.objects.get_or_create(name=district_text)
        self.location.district = district

        self.location.save()
        self.parse_location_programs(self.location)

    def parse_location_programs(self, location):
        location.facilities.delete

