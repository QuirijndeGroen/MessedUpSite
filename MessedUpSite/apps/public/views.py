from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from MessedUpSite.apps.activityapi.models import Activity


def index(request: HttpRequest) -> HttpResponse:
    next_activity = (
        Activity.objects.filter(is_active=True).order_by("start_time").first()
    )
    return render(request, "index.html", {"next_activity": next_activity})


def floorball(request: HttpRequest) -> HttpResponse:
    return render(request, "floorball.html")


def association(request: HttpRequest) -> HttpResponse:
    return render(request, "association.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "contact.html")
