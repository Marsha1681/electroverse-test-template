# from django.db import models

# Create your models here.
from django.db import models


class Location(models.Model):
    reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    operator_reference = models.CharField(max_length=100)
    country_reference = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EVSE(models.Model):
    location = models.ForeignKey(Location, related_name="evses", on_delete=models.CASCADE)
    physical_identifier = models.CharField(max_length=100)
    status = models.CharField(max_length=50)


class Connector(models.Model):
    evse = models.ForeignKey(EVSE, related_name="connectors", on_delete=models.CASCADE)
    power = models.IntegerField()
    standard = models.CharField(max_length=50)
