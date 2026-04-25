from django.urls import path

from . import views


app_name = "public"
urlpatterns = [
    path("", views.index, name="index"),
    path("floorball/", views.floorball, name="floorball"),
    path("association/", views.association, name="association"),
    path("contact/", views.contact, name="contact"),
]
