from django.test import TestCase
from django.core.management import call_command
from src.task.models import Location, EVSE, Connector

class ImportDataTest(TestCase):
    def test_import_creates_data(self):
        call_command("import_data")

        self.assertGreater(Location.objects.count(), 0)
        self.assertGreater(EVSE.objects.count(), 0)
        self.assertGreater(Connector.objects.count(), 0)

class LocationAPITest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            latitude=50.0,
            longitude=-1.0,
            postal_code="TEST",
            operator_reference="TEST",
            country_reference="GBR",
        )

        self.evse = EVSE.objects.create(
            location=self.location,
            physical_identifier="EVSE-1",
            status="UNKNOWN",
        )

        Connector.objects.create(
            evse=self.evse,
            power=50,
            standard="IEC_62196_T2",
        )

    # List tests
    def test_location_list_status_code(self):
        response = self.client.get("/task/locations/")
        self.assertEqual(response.status_code, 200)

    def test_location_list_has_wrapper(self):
        response = self.client.get("/task/locations/")
        data = response.json()

        self.assertIn("locations", data)
        self.assertIsInstance(data["locations"], list)

    def test_location_list_structure(self):
        response = self.client.get("/task/locations/")
        location = response.json()["locations"][0]

        self.assertIn("coordinates", location)
        self.assertIn("operator_reference", location)
        self.assertIn("country_reference", location)
        self.assertIn("postal_code", location)
        self.assertIn("number_of_evses", location)

        self.assertIn("lat", location["coordinates"])
        self.assertIn("lon", location["coordinates"])

    def test_number_of_evses_is_correct(self):
        response = self.client.get("/task/locations/")
        location = response.json()["locations"][0]

        self.assertEqual(location["number_of_evses"], 1)

    # Detail tests
    def test_location_detail_status_code(self):
        response = self.client.get(f"/task/locations/{self.location.id}/")
        self.assertEqual(response.status_code, 200)

    def test_location_detail_coordinates(self):
        response = self.client.get(f"/task/locations/{self.location.id}/")
        coords = response.json()["coordinates"]

        self.assertEqual(coords["lat"], 50.0)
        self.assertEqual(coords["lon"], -1.0)

    def test_location_detail_evses_structure(self):
        response = self.client.get(f"/task/locations/{self.location.id}/")
        evses = response.json()["evses"]

        self.assertIsInstance(evses, list)
        self.assertEqual(len(evses), 1)

        evse = evses[0]

        self.assertIn("physical_identifier", evse)
        self.assertIn("status", evse)
        self.assertIn("connectors", evse)

    def test_connector_structure(self):
        response = self.client.get(f"/task/locations/{self.location.id}/")
        connector = response.json()["evses"][0]["connectors"][0]

        self.assertIn("power", connector)
        self.assertIn("standard", connector)