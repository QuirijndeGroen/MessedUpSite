from django.http import HttpRequest
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from MessedUpSite.apps.activityapi.models import Activity


@login_required(login_url="/accounts/login/")
def ProfileView(request: HttpRequest):
    return TemplateView.as_view(template_name="accounts/profile.html")(request)


@login_required(login_url="/accounts/login/")
def MembersView(request: HttpRequest):
    activities = Activity.objects.filter(is_active=True, type="activity").order_by(
        "start_time"
    )
    tournaments = Activity.objects.filter(is_active=True, type="tournament").order_by(
        "start_time"
    )
    return render(
        request,
        "accounts/members.html",
        {"activities": activities, "tournaments": tournaments},
    )
