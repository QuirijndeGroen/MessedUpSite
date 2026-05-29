from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from MessedUpSite.apps.activities.models import Activity
from MessedUpSite.apps.registrationlists.forms import RegistrationForm


def index(request: HttpRequest) -> HttpResponse:
    try:
        next_activities = Activity.objects.all().order_by("start_time")
        next_activities = [
            activity for activity in next_activities if activity.is_active
        ]
        next_public_activities = [
            activity for activity in next_activities if activity.public
        ]
        if len(next_public_activities) > 0:
            next_activity = next_public_activities[0]
        else:
            next_activity = next_activities[0] if len(next_activities) > 0 else None

    except Activity.DoesNotExist:
        next_activity = None

    return render(request, "index.html", {"next_activity": next_activity})


def floorball(request: HttpRequest) -> HttpResponse:
    return render(request, "floorball.html")


def association(request: HttpRequest) -> HttpResponse:
    return render(request, "association.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "contact.html")


def public_activity(request: HttpRequest, pk: int):
    activity = Activity.objects.filter(id=pk, public=True).prefetch_related(
        "registrationlists__questions"
    )
    activity = [activity for activity in activity if activity.is_active]

    for activity in activity:
        for registrationlist in activity.registrationlists.all():
            registrationlist.form = RegistrationForm(
                questions=registrationlist.questions.all()
            )

    return render(
        request,
        "public_activity.html",
        {"activity": activity},
    )
