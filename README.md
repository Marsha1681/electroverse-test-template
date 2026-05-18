# Octopus Electroverse – Tech Task
This project is a Django REST API for importing and exposing EV charging location data.

# Implemented features:
-Import data from integrated.json
-Store locations, EVSEs, and connectors
-List all locations
-Retrieve a single location detail
-Django admin interface
-Tests

# Tech Stack
-Python
-Django
-Django REST Framework
-SQLite

# API Endpoints
List Locations- GET /task/locations/
-Returns all charging locations in the required format.

Location Detail- GET /task/locations/<id>/
-Returns a detailed view of a single location including EVSEs and connectors.

# Running the Project
Install dependencies- pip install -r requirements.txt
Run migrations- python manage.py migrate
Import data- python manage.py import_data
Create admin user -python manage.py createsuperuser
Start server- python manage.py runserver
Admin Interface- Accessible at: http://127.0.0.1:8000/admin/

# The admin panel allows viewing and managing:
-Locations
-EVSEs
-Connectors
-Tests

Run tests with: python manage.py test

# Tests cover:
-data importing
-location list endpoint
-location detail endpoint

# Notes
-Missing operator references default to "UNKNOWN"
-number_of_evses is generated using queryset annotations
-SQLite was used for simplicity