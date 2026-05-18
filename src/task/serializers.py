from rest_framework import serializers
from .models import Location, EVSE, Connector

class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = ["power", "standard"]

class EVSESerializer(serializers.ModelSerializer):
    connectors = ConnectorSerializer(many=True)

    class Meta:
        model = EVSE
        fields = ["physical_identifier", "status", "connectors"]

class LocationListSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()
    number_of_evses = serializers.IntegerField(read_only=True)

    class Meta:
        model = Location
        fields = [
            "coordinates",
            "operator_reference",
            "country_reference",
            "postal_code",
            "number_of_evses",
        ]

    def get_coordinates(self, obj):
        return {
            "lat": obj.latitude,
            "lon": obj.longitude,
        }

class LocationDetailSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()
    evses = EVSESerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = [
            "coordinates",
            "operator_reference",
            "country_reference",
            "postal_code",
            "evses",
        ]

    def get_coordinates(self, obj):
        return {
            "lat": obj.latitude,
            "lon": obj.longitude,
        }