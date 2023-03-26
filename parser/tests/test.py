from django.test import TestCase
from parser.services.location_parser import LocationParser
import datetime

class LocationParserTestCase(TestCase):
    def test_unpack_program_str(self):
        lower_str = "Leisure Skate (16yrs and over)"
        upper_str = "Leisure Skate (up to 12yrs)"
        both_str = "Leisure Skate (16 - 55yrs)"
        none_str = "Leisure Skate"

        self.assertEqual(LocationParser.unpack_program_str(lower_str), ["Leisure Skate", 16, 99])
        self.assertEqual(LocationParser.unpack_program_str(upper_str), ["Leisure Skate", 1, 12])
        self.assertEqual(LocationParser.unpack_program_str(both_str), ["Leisure Skate", 16, 55])
        self.assertEqual(LocationParser.unpack_program_str(none_str), ["Leisure Skate", 1, 99])

    def test_unpack_time_str(self):
        am_str = "7:15 - 8:15am"
        pm_str = "7:15 - 8:15pm"
        mixed_str = "11:30am - 2:30pm"
        hr_str = "7:30am - 10pm"

        self.assertEqual(LocationParser.unpack_time_str(am_str), [datetime.time(7, 15), datetime.time(8, 15)])
        self.assertEqual(LocationParser.unpack_time_str(pm_str), [datetime.time(19, 15), datetime.time(20, 15)])
        self.assertEqual(LocationParser.unpack_time_str(mixed_str), [datetime.time(11, 30), datetime.time(14, 30)])
        self.assertEqual(LocationParser.unpack_time_str(hr_str), [datetime.time(7, 30), datetime.time(22, 00)])
