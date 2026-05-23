from django.apps import AppConfig


class QuotesConfig(AppConfig):
    name = 'MessedUpSite.apps.quotes'
    label = 'quotes'
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Manage Quotes"
    