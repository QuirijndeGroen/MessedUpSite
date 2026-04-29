from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MessedUpSite.apps.registrationlists.forms import RegistrationForm
from .models import Activity


@login_required(login_url="/accounts/login/")
def ActivitiesView(request: HttpRequest):
    activities = Activity.objects.filter(is_active=True).order_by("start_time").prefetch_related(
        "registrationlists__questions"
    )

    for activity in activities:
        for registrationlist in activity.registrationlists.all():
            registrationlist.form = RegistrationForm(questions=registrationlist.questions.all())

    return render(
        request,
        "accounts/activities.html",
        {"activities": activities},
    )
