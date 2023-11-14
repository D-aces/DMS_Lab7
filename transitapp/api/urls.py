from django.urls import path
from transitapp.api.views import api_get_defined_bus_trip

app_name = 'transit_api_extension'

urlpatterns = [
    path('start<start>/stop<stop>', api_get_defined_bus_trip, name="detail")
]