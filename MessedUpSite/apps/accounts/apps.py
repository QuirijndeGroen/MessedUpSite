from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "MessedUpSite.apps.accounts"
    label = "accounts"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Manage Accounts and User Rights"
