from django.urls import path

from . import views

urlpatterns = [
    # Views
    path('', views.index, name='home'),

    # React components
    path('api/facilities', views.facilities, name='api-facilities')
]
