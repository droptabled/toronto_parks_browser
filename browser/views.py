from django.shortcuts import render
from django.http import JsonResponse
from parser.models import *


def index(request):
    return render(request, "browser/index.html")

def facilities(request):
    data = { "facilities": []}
    for facility in Facility.objects.prefetch_related("tiers"):
        facility_data = {
            "id": facility.id,
            "name": facility.name,
            "link": facility.page_link(),
            "image_link": facility.image_url,
            "alt_text": facility.alt_text,
            "available_tiers": []
        }

        for tier in facility.tiers.all():
            facility_data["available_tiers"].append(tier.tier)

        data["facilities"].append(facility_data)
    return JsonResponse(data)