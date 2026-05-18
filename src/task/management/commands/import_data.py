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

            op = item.get("operator")

            if isinstance(op, dict):
                operator_reference = op.get("name") or op.get("id") or ""
            else:
                operator_reference = op or "UNKNOWN"

            location = Location.objects.create(
                reference=item.get("reference"),
                operator_reference=operator_reference,
                country_reference=item.get("country", "") or "",
                postal_code=item.get("postal_code", ""),
                latitude=latitude,
                longitude=longitude,
            )

            seen_evses = set()

            for evse_data in item.get("evses", []):
                key = evse_data["physical_reference"]

                if key in seen_evses:
                    continue

                seen_evses.add(key)

                evse, _ = EVSE.objects.get_or_create(
                    physical_identifier=key,
                    location=location,
                    defaults={
                        "status": evse_data.get("status", "UNKNOWN"),
                    }
                )

            for evse_data in item.get("evses", []):
                evse, _ = EVSE.objects.get_or_create(
                    physical_identifier=evse_data["physical_reference"],
                    location=location,
                    defaults={
                        "status": evse_data.get("status", "UNKNOWN"),
                    }
                )

                for conn in evse_data.get("connectors", []):
                    Connector.objects.get_or_create(
                        evse=evse,
                        power=conn.get("power") or conn.get("power_kw") or 0,
                        standard=conn.get("standard") or "UNKNOWN",
                    )

        self.stdout.write(self.style.SUCCESS("Import complete"))
        