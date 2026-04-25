from django.db import models


class UserPersona(models.Model):
    """Represents a user persona."""

    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Represents a user profile, which can be associated with a user."""

    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, related_name="profile"
    )
    is_full_name_displayed = models.BooleanField(default=True)

    persona = models.ForeignKey(
        UserPersona, on_delete=models.SET_NULL, null=True, blank=True
    )
