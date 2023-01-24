from django.urls import path

from . import views

urlpatterns = [
    # Views
    path('', views.index, name='home'),

    # React components
    path('api/facils', views.facils, name='api-facils')
]
