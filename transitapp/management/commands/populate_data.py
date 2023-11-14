import requests
import environ
from django.core.management.base import BaseCommand
from transitapp.models import Destination, Route, Stops, bus_traffic_details
from transitapp.data.api_urls import api_urls
from django.template import loader

env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    def handle(self, *args, **options):
        #Import Data from External MyBus API
        jsonfile_0 = requests.get(api_urls[0])
        jsonfile_1 = requests.get(api_urls[1])
        jsonfile_2 = requests.get(api_urls[2])

        #Convert to Python Dict Structure
        bus_routes = jsonfile_0.json()
        bus_stops = jsonfile_1.json()
        bus_destinations = jsonfile_2.json()

        #Create an empty list to store the objects
        routes = []
        stops = []
        destinations = []

        # iterate through the entire dict struct, creating objects and records in the table
        for destination in bus_destinations['destinations']:
            #Creates a destination object for each record of a destination in the JSON file
            if not Destination.objects.filter(destination_number = destination['number']).exists():
                get_bus_specific_dest = requests.get(api_urls[3] + str(destination['number']) + '?auth_token=' + env('MyBusAPI_AUTH_TOKEN'))
                ind_destination = get_bus_specific_dest.json()
                destination_obj = Destination.objects.create(destination_number=destination['number'], destination_name=ind_destination['destination']['name'])
                destinations.append(destination_obj)
          
        for stop in bus_stops['stops']:
            #Creates a stop object for each record of a stop in the JSON file
            if not Stops.objects.filter(stop_number = stop['number']).exists():
                stop_obj = Stops.objects.create(stop_number=stop['number'], name=stop['name'], latitude=stop['latitude'], longitude=stop['longitude'])
                stops.append(stop_obj)

        for route in bus_routes['routes']:
            #Creates a route object for each record of a route in the JSON file
            if not Route.objects.filter(route_number = route['number']).exists():
                route_obj = Route.objects.create(route_number=route['number'])
                routes.append(route_obj)
        
        self.stdout.write(self.style.SUCCESS(f'Successully created {len(routes)} routes, {len(stops)} stops, and {len(destinations)} destinations.'))

       





