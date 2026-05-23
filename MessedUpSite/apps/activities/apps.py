from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    name = "MessedUpSite.apps.activities"
    label = "activities"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Manage Activities, Tournaments and Polls"
