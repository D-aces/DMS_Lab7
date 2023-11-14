from rest_framework import serializers
from transitapp.models import Stops, bus_traffic_details


class TransitSerializer(serializers.ModelSerializer):
    class Meta:
        model = bus_traffic_details
        fields = ['route', 'destination__destination_name']