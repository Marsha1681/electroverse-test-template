from django.urls import path
from .views import LocationListView, LocationDetailView

urlpatterns = [

    path("locations/", LocationListView.as_view()),
    path("locations/<int:pk>/", LocationDetailView.as_view()),
]