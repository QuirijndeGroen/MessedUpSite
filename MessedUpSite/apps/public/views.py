from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from MessedUpSite.apps.activities.models import Activity
from MessedUpSite.apps.registrationlists.forms import RegistrationForm


def index(request: HttpRequest) -> HttpResponse:
    try:
        next_activity = (
            Activity.objects.filter(is_active=True).order_by("start_time").first()
        )
        return render(request, "index.html", {"next_activity": next_activity})
    except Activity.DoesNotExist:
        return render(request, "index.html", {"next_activity": None})


def floorball(request: HttpRequest) -> HttpResponse:
    return render(request, "floorball.html")


def association(request: HttpRequest) -> HttpResponse:
    return render(request, "association.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "contact.html")

def public_activity(request: HttpRequest, pk: int):
    activity = Activity.objects.filter(is_active=True, id=pk, public=True).prefetch_related("registrationlists__questions")

    for activity in activity:
        for registrationlist in activity.registrationlists.all():
            registrationlist.form = RegistrationForm(questions=registrationlist.questions.all())


    return render(
        request,
        "public_activity.html",
        {"activity": activity},
    )


