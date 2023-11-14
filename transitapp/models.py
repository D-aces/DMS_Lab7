from django.db import models

#Creating the Bus_Routes Model
class Destination(models.Model):
    destination_number = models.BigIntegerField(primary_key=True)
    destination_name = models.CharField(max_length=255)

class Route(models.Model):
    route_number = models.BigIntegerField(primary_key=True)

#Creating the Bus_Stops Model
class Stops(models.Model):
    stop_number = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    bus_routes = models.ManyToManyField(Route, through='bus_traffic_details')
    #Returns the bus stop number and name (to distinguish stops with the same name, on opposite sides of the road)
    def __string__(self):
        return self.stop_number + ' ' + self.name

#Define many-to-many table for bus stops and bus routes (shows all the bus traffic for different stop + route combinations)
class bus_traffic_details(models.Model):
    Route = models.ForeignKey("Route", on_delete=models.CASCADE)
    stops = models.ForeignKey("Stops", on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    passing_time = models.DateTimeField()

