from django.urls import path

from . import views

urlpatterns = [
    # Views
    path('', views.index, name='home'),
    path('facilities', views.facilities, name='facilities'),
    path('test', views.test),

    # API for React components
    path('api/facilities', views.api_facilities, name='api-facilities'),
]
