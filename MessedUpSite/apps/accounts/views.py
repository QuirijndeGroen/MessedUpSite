from django.http import HttpRequest
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from MessedUpSite.apps.documents.models import Document
from MessedUpSite.apps.activities.models import Activity
from .models import User


@login_required(login_url="/accounts/login/")
def ProfileView(request: HttpRequest):
    
    user = request.user
    committees = user.committees.values_list('name', flat=True)

    return render(request, "accounts/profile.html", {"user": user, "committees": committees})


@login_required(login_url="/accounts/login/")
def MembersView(request: HttpRequest):
    try:
        activities = Activity.objects.filter(type="activity").order_by("start_time")
        activities = [activity for activity in activities if activity.is_active]
    except Activity.DoesNotExist:
        activities = None

    try:
        tournaments = Activity.objects.filter(type="tournament").order_by("start_time")
        tournaments = [tournament for tournament in tournaments if tournament.is_active]
    except Activity.DoesNotExist:
        tournaments = None

    try:
        documents = Document.objects.all().order_by("created")
    except Document.DoesNotExist:
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

    user_rights = request.user.committees.values_list('name', flat=True).values_list("rights", flat=True)

    if "Full" in user_rights:
        activities = Activity.objects.all().order_by("start_time").prefetch_related(
            "registrationlists__questions"
        )
        documents = Document.objects.all().order_by("title")

        users = User.objects.all().order_by("username")
    
    elif request.user.committees.exists():
        for committee in request.user.committees.values_list('name', flat=True):
            committee_rights = committee.rights.all()

            if "Document & Activity" in committee_rights:
                activities = Activity.objects.filter(organizer=committee).order_by("start_time").prefetch_related(
                    "registrationlists__questions"
                )
                documents = Document.objects.all().order_by("title")

                users = None
                
            elif "Activity" in committee_rights:
                activities = Activity.objects.filter(organizer=committee).order_by("start_time").prefetch_related(
                    "registrationlists__questions"
                )

                documents = None
                users = None
    
    else:
        activities = None
        documents = None
        users = None


    return render(
    request,
    "accounts/add_content.html",
    {
        "activities": activities,
        "documents": documents,
        "users": users,
        },
    )


