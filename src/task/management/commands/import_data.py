import json
from pathlib import Path
from django.core.management.base import BaseCommand
from src.task.models import Location, EVSE, Connector


class Command(BaseCommand):
    help = "Import integrated data"

    def handle(self, *args, **kwargs):
        file_path = Path("data") / "integrated.json"

        with open(file_path) as f:
            data = json.load(f)

        for item in data:
            coords = item.get("coordinates", {})

            latitude = (
                coords.get("lat")
                or coords.get("latitude")
            )

            longitude = (
                coords.get("lon")
                or coords.get("lng")
                or coords.get("longitude")
            )

            location = Location.objects.create(
                reference=item.get("reference"),
                operator_reference=item.get("operator_reference", ""),
                country_reference=item.get("country_reference", ""),
                postal_code=item.get("postal_code", ""),
                latitude=latitude,
                longitude=longitude,
            )

            for evse_data in item.get("evses", []):
                evse = EVSE.objects.create(
                    location=location,
                    physical_identifier=evse_data.get("physical_reference", ""),
                    status=evse_data.get("status", ""),
                )

                for conn in evse_data.get("connectors", []):
                    Connector.objects.create(
                        evse=evse,
                        power=conn.get("power", 0),
                        standard=conn.get("standard", ""),
                    )

        self.stdout.write(self.style.SUCCESS("Import complete"))