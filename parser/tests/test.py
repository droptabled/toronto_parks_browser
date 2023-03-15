from django.test import TestCase
from parser.services.location_parser import LocationParser

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
