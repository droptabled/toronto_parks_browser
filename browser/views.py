from django.shortcuts import render

from django.template import loader
from django.http import HttpResponse


def index(request):
    return render(request, "browser/index.html")

def facilities(request):
    return render(request, "browser/facilities.html")