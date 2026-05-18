from rest_framework import generics 
from rest_framework.response import Response
from .models import Location
from .serializers import LocationListSerializer, LocationDetailSerializer
from django.db.models import Count


class LocationListView(generics.ListAPIView):
    serializer_class = LocationListSerializer
    def get_queryset(self):
        
        queryset = Location.objects.all().annotate(
            number_of_evses=Count("evses")
        )

        country = self.request.query_params.get("country")
        operator = self.request.query_params.get("operator")

        if country:
            queryset = queryset.filter(country_reference=country)

        if operator:
            queryset = queryset.filter(operator_reference=operator)

        ordering = self.request.query_params.get("ordering")
        if ordering in ["created_at", "-created_at", "updated_at", "-updated_at"]:
            queryset = queryset.order_by(ordering)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "locations": serializer.data
        })

class LocationDetailView(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer