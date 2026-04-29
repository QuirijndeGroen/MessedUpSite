from django.urls import path
from . import views

app_name = "registrationlists"

urlpatterns = [
    path(
        "registrationlists/<int:pk>/register/",
        views.submit_registration,
        name="registration_submit",
    ),
    path(
        "registrationlists/<int:pk>/responses/",
        views.view_responses,
        name="view_responses",
    ),
]
