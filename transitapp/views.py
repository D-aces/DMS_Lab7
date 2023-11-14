import requests
import datetime
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from transitapp.forms import Stopform
from transitapp.models import Stops, Route, bus_traffic_details, Destination


def home(request):
    context = {}
    form = Stopform()
    stops = Stops.objects.all()
    context['stops'] = stops
    context['form'] = form
    return render(request, 'homepage.html', context)

def bus_routes(request):
    context = {}
    starting_point = request.POST.get('starting_point', None)
    destination = request.POST.get('destination', None)

    context['starting_point'] = starting_point
    context['destination'] = destination

    # Had to do major filtering here, and there was no existing method/function for finding distinct values of destination_number 
    valid_bus_routes = bus_traffic_details.objects.filter(
    Route__route_number__in=bus_traffic_details.objects.filter(
        stops__stop_number=starting_point.split(':')[0]
    ).values('Route__route_number')
    ).filter(
    Route__route_number__in=bus_traffic_details.objects.filter(
        stops__stop_number=destination.split(':')[0]
    ).values('Route__route_number')
    )

    route_details = valid_bus_routes.values('Route__route_number','destination__destination_number', 'destination__destination_name', 'stops__stop_number', 'stops__name', 'passing_time')
    context['route_details'] = route_details

    unique_routes = set()
    unique_route_numbers = set()
    unique_route_details = []

    for route_detail in route_details:
        key = (route_detail['destination__destination_number'], route_detail['stops__stop_number'])
        route_number = route_detail['Route__route_number']

        # Check if the key is unique and route number is not seen before
        if key not in unique_routes and route_number not in unique_route_numbers:
            unique_routes.add(key)
            unique_route_numbers.add(route_number)
            unique_route_details.append(route_detail)

    context['unique_route_details'] = unique_route_details
    return render(request, "transit_route_select.html", context)

def bus_route_detail(request):
    context = {}

    current_datetime = datetime.datetime.now()

    starting_point = request.POST.get('starting_point', None)
    destination = request.POST.get('destination', None)
    route_name_num = request.POST.get('route_name_num', None)
    route_details = request.POST.get('route_details', None)

    context['starting_point'] = starting_point
    context['destination'] = destination
    context['route_name_num'] = route_name_num
    context['route_details'] = route_details

    route_progress = bus_traffic_details.objects.filter(
        Route__route_number__in=bus_traffic_details.objects.filter(
            stops__stop_number=starting_point.split(':')[0]
        ).values('Route__route_number')
    ).filter(
        Route__route_number__in=bus_traffic_details.objects.filter(
            stops__stop_number=destination.split(':')[0]
        ).values('Route__route_number')
    ).filter(
        Route__route_number=route_name_num.split(":")[1],
        passing_time__gte=current_datetime
    ).order_by('passing_time')

    context['route_progress'] = route_progress

    return render(request, "transit_route_details.html", context)