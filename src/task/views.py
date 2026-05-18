from rest_framework import generics
from .models import Location
from .serializers import LocationListSerializer, LocationDetailSerializer


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer


class LocationDetailView(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer