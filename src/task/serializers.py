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
    number_of_evses = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "id",
            "latitude",
            "longitude",
            "operator_reference",
            "country_reference",
            "postal_code",
            "number_of_evses",
        ]

    def get_number_of_evses(self, obj):
        return obj.evses.count()

class LocationDetailSerializer(serializers.ModelSerializer):
    evses = EVSESerializer(many=True)

    class Meta:
        model = Location
        fields = [
            "id",
            "latitude",
            "longitude",
            "operator_reference",
            "country_reference",
            "postal_code",
            "evses",
        ]