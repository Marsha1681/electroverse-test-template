from django.contrib import admin
from .models import Location, EVSE, Connector

class EVSEInline(admin.TabularInline):
    model = EVSE
    extra = 0

class ConnectorInline(admin.TabularInline):
    model = Connector
    extra = 0

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "operator_reference",
        "country_reference",
        "postal_code",
        "latitude",
        "longitude",
    )
    inlines = [EVSEInline]

@admin.register(EVSE)
class EVSEAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "physical_identifier", "status")
    inlines = [ConnectorInline]

@admin.register(Connector)
class ConnectorAdmin(admin.ModelAdmin):
    list_display = ("id", "evse", "power", "standard")