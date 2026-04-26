from django.urls import path
from . import views


name = "activities"
urlpatterns = [
    path("activities/", views.ActivitiesView, name="activities"),
]
