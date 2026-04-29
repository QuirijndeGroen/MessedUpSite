from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MessedUpSite.apps.registrationlists.models import RegistrationList
from .models import Activity


@login_required(login_url="/accounts/login/")
def ActivitiesView(request: HttpRequest):
    activities = Activity.objects.filter(is_active=True).order_by("start_time")
    registrationlists = RegistrationList.objects.all()
    return render(
        request,
        "accounts/activities.html",
        {"activities": activities, "registrtionlists": registrationlists},
    )
