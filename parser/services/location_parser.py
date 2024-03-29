from datetime import date, datetime
import re
from parser.models import *

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

class LocationParser:
    """Parsing info for a specific location"""

    def __init__(self, url: str):
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
        self.parse_programs()

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

    def parse_programs(self):
        programs_tab = self.main_page.find("div", id="pfrComplexTabs-dropin")
        category_tabs = programs_tab.find_all("div", id=re.compile("content_dropintype_.*"))

        for category_tab in category_tabs:
            category_name = category_tab.attrs['id'].split('_')[-1]
            category, _ = ProgramCategory.objects.get_or_create(name=category_name)

            weekly_tabs = category_tab.find_all("tr", id=re.compile("dropin_.*"))
            for weekly_tab in weekly_tabs:
                table = weekly_tab.find("table")
                # remove first cell of dates since its the program header
                dates_text = [cell.text for cell in table.thead.find_all("th")][1:]
                # parse the dates, and then delete all old programs on those dates
                dates = []
                for date_text in dates_text:
                    date = datetime.strptime(f"{date_text} {datetime.today().year}", "%a %b %d %Y").date()
                    dates.append(date)
                    ProgramInstance.objects.filter(date=date, location=self.location).delete()

                program_rows = table.tbody.find_all("tr")
                for program_row in program_rows:
                    program_name, lower_age, upper_age = self.unpack_program_str(program_row.find("th").text)
                    program, _ = Program.objects.get_or_create(program_category=category, name=program_name, is_drop_in=True)
                    cells = program_row.find_all("td")

                    program_details = {
                        "location": self.location,
                        "program": program,
                        "lower_age": lower_age,
                        "upper_age": upper_age,
                    }

                    self.assign_times(program_details, dates, cells)
        return True

    # takes some ProgramInstance args and a set of dates and times
    # creates one new ProgramInstance for each time interval
    def assign_times(self, program_details: dict, dates: list[date], week_cells: ResultSet):
        week_times = [self.split_times(week_cell) for week_cell in week_cells]
        program_instance_list = []

        for idx, day_times in enumerate(week_times):
            program_date = dates[idx]

            for program_time in day_times:
                start_time, end_time = self.unpack_time_str(program_time)
                program_instance_list.append(
                    ProgramInstance(
                        date=program_date,
                        start_time=start_time,
                        end_time=end_time,
                        **program_details
                    )
                )

        ProgramInstance.objects.bulk_create(program_instance_list)

    # split <hr> separated BeautifulSoup td cell into array of times
    @staticmethod
    def split_times(cell: Tag):
        children = [child.text.strip() for child in cell.children if child.text.strip()]
        return children

    # split string description of program into a name and age range
    # returns program_name, lower_age, upper_age
    @staticmethod
    def unpack_program_str(str: str):
        # split based on ( and )
        split_arr = re.split('[\(\)]', str)
        program_name = split_arr[0].strip()
        lower = 1
        upper = 99

        # if there aren't any parens, no age limit is given, so apply defaults
        if len(split_arr) <= 1:
            return [program_name, lower, upper]

        age_str = split_arr[1]
        match_found = False

        # TODO: figure out a better way to switch case this somehow?
        lower_and_upper_match = re.match(r'(\d+) \- (\d+)yrs', age_str)
        if lower_and_upper_match:
            lower = lower_and_upper_match.group(1)
            upper = lower_and_upper_match.group(2)
            match_found = True

        lower_match = re.match(r'(\d+)yrs and over', age_str)
        if lower_match and not match_found:
            lower = lower_match.group(1)
            match_found = True

        upper_match = re.match(r'up to (\d+)yrs', age_str)
        if upper_match and not match_found:
            upper = upper_match.group(1)
            match_found = True

        return [program_name, int(lower), int(upper)]

    # split string of program time str into a start and end datetime.time
    # returns start time, end time
    @staticmethod
    def unpack_time_str(str: str):
        start_str, end_str = str.split('-')
        start_str = start_str.strip()
        end_str = end_str.strip()

        # the end time always has a meridian indicator (am/pm)
        end_time = LocationParser.str_to_time(end_str)
        # if start time does not have a meridian indicator if it is the same as the end
        start_12h = re.search("[A-Za-z]+", start_str)
        if not start_12h:
            end_12h = re.search("[A-Za-z]+", end_str).group(0)
            start_str = start_str + end_12h
        start_time = LocationParser.str_to_time(start_str)

        return [start_time, end_time]

    # convert string to time, using the different city of toronto time formats
    @staticmethod
    def str_to_time(str: str):
        for fmt in ("%I:%M%p", '%I%p'):
            try:
                return datetime.strptime(str, fmt)
            except ValueError:
                pass
        raise "Coulding find time"
