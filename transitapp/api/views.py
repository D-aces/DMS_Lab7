import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from transitapp.models import bus_traffic_details, Route
from transitapp.api.serializer import TransitSerializer

@api_view(['GET'])
def api_get_defined_bus_trip(request, start, stop):
        starting_routes = Route.objects.filter(
            bus_traffic_details__stops__stop_number=start
        )

        stopping_routes = Route.objects.filter(
            bus_traffic_details__stops__stop_number=stop
        )

        common_routes = starting_routes.filter(pk__in=stopping_routes)

        result = {
            route.route_number: route.bus_traffic_details_set.filter(stops__stop_number=start).first().destination.destination_name
            for route in common_routes
        }

        return Response(result)