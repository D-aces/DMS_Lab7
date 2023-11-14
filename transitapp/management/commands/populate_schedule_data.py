import requests
import environ
from django.core.management.base import BaseCommand
from transitapp.models import Destination, Route, Stops, bus_traffic_details
from transitapp.data.api_urls import api_urls

env = environ.Env()
environ.Env.read_env()

# Don't run this program for too long, it's a lot of data (kill it when you feel it has populated enough) : It will create 6k+ records
#Created a seperate file, as normally this data would need to have frequent connections to the MyBus API (this is a placeholder to 
# populate schedule data [for now])
class Command(BaseCommand):
    def handle(self, *args, **options):
        jsonfile = requests.get(api_urls[1])
        bus_stops = jsonfile.json()
        stop_details = []

        for stop in bus_stops['stops']:
            count = 1
            #Dealing with invalid api routes (Stop 1030, 1135, 1246, etc. does not return a valid response), will skip over them
            try:
                get_bus_specific_stop_details = requests.get(api_urls[4] + str(stop['number']) + '?auth_token=' + env('MyBusAPI_AUTH_TOKEN'))
                ind_stop = get_bus_specific_stop_details.json()
                hold_stop_num = stop['number']

                self.stdout.write(self.style.SUCCESS(f"For stop number {stop['number']}..."))
                for route in ind_stop['stop']['calls']:
                    #Place Holder so the if statement will work
                    route_number = route['route']
                    #Dealing with 1 Tricky Mainline issue (where 1 is the mainline bus route split into 2 subroutes: Downtown to New Sudbury, Downtown to South End)
                    if 'N' in route['route'] or 'S' in route['route']:
                        route_number = route['route'][0]
                    stops_detail_obj = bus_traffic_details.objects.create(Route=Route.objects.get(route_number=route_number), stops=Stops.objects.get(stop_number=hold_stop_num), 
                                                    destination=Destination.objects.get(destination_number=route['destination']['number']), passing_time=route['passing_time'])
                    stop_details.append(stops_detail_obj)
            
                    self.stdout.write(f"Created {count} new record(s)")
                    count+=1
            except:
                continue
        self.stdout.write(self.style.SUCCESS(f'Successully created {len(stop_details)} stop_bus_traffic details'))

       


