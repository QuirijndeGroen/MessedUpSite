from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def floorball(request: HttpRequest) -> HttpResponse:
    return render(request, "floorball.html")


def association(request: HttpRequest) -> HttpResponse:
    return render(request, "association.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "contact.html")
