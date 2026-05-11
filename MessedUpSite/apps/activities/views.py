from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MessedUpSite.apps.registrationlists.forms import RegistrationForm
from MessedUpSite.apps.registrationlists.models import RegistrationResponses
from .models import Activity


@login_required(login_url="/accounts/login/")
def ActivitiesView(request: HttpRequest):
    activities = Activity.objects.order_by("start_time").prefetch_related(
        "registrationlists__questions"
    )
    activities = [activity for activity in activities if activity.is_active]

    # Get all registration responses for the current user
    user_registrations = RegistrationResponses.objects.filter(user=request.user).values_list(
        'linked_registrationlist_id', flat=True
    )

    for activity in activities:
        for registrationlist in activity.registrationlists.all():
            registrationlist.form = RegistrationForm(questions=registrationlist.questions.all())
            registrationlist.user_registered = registrationlist.id in user_registrations

    return render(
        request,
        "accounts/activities.html",
        {"activities": activities},
    )
