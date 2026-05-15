from django.http import HttpRequest
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MessedUpSite.apps.documents.models import Document
from MessedUpSite.apps.activities.models import Activity


@login_required(login_url="/accounts/login/")
def ProfileView(request: HttpRequest):
    return TemplateView.as_view(template_name="accounts/profile.html")(request)


@login_required(login_url="/accounts/login/")
def MembersView(request: HttpRequest):
    try:
        activities = Activity.objects.filter(type="activity").order_by(
            "start_time"
        )
        activities = [activity for activity in activities if activity.is_active]
    except Activity.DoesNotExist:
        activities = None

    try:
        tournaments = Activity.objects.filter(type="tournament").order_by(
            "start_time"
            )
        tournaments = [tournament for tournament in tournaments if tournament.is_active]
    except Activity.DoesNotExist:
        tournaments = None

    try:
        documents = Document.objects.all().order_by("created")
    except:
        documents = None

    return render(
        request,
        "accounts/members.html",
        {
            "activities": activities,
            "tournaments": tournaments,
            "documents": documents,
        },
    )


@login_required(login_url="/accounts/login/")
def AddContentView(request: HttpRequest):

    user_committees = request.user.committees.all()

    for group in user_groups:
        if "activities" in group.rights.all():
            Can create activities and registrationlists.
        if "documents" in group.rights.all():
            Can create documents.
        if "users" in group.rights.all():
            Can create users.

    return TemplateView.as_view(template_name="accounts/create.html")(request)