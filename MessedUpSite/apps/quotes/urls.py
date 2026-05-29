from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path(
        "quotes/",
        views.quote_list,
        name="quote_list",
    ),
]
