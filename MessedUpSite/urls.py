from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("MessedUpSite.apps.public.urls")),
    path("accounts/", include("MessedUpSite.apps.accounts.urls")),
]
