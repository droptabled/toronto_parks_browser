from django.shortcuts import render
from django.http import JsonResponse
from parser.models import *
from parser.services.location_parser import LocationParser


def index(request):
    return render(request, "browser/index.html")

def facilities(request):
    return render(request, "browser/facilities.html")

def api_facilities(request):
    data = { "facilities": []}
    for facility in Facility.objects.prefetch_related("tiers"):
        facility_data = {
            "id": facility.id,
            "name": facility.name,
            "link": facility.page_link(),
            "imageLink": facility.image_url,
            "altText": facility.alt_text,
            "availableTiers": []
        }

        for tier in facility.tiers.all():
            facility_data["availableTiers"].append(tier.tier)

        data["facilities"].append(facility_data)
    return JsonResponse(data)

def test(request):
    location = LocationParser("https://www.toronto.ca/data/parks/prd/facilities/complex/499/index.html")
    location.parse_location()
    return JsonResponse({"done": "done"})