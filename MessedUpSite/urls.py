from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("MessedUpSite.apps.public.urls")),
    path("accounts/", include("MessedUpSite.apps.accounts.urls")),
    path("accounts/", include("MessedUpSite.apps.activities.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
document_root = settings.MEDIA_ROOT
