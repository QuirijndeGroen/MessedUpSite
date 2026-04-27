from django.db import models
from rest_framework.fields import BooleanField, DateTimeField, EmailField, IntegerField
from MessedUpSite.apps.activities.models import Activity


class ActivityField(models.IntegerField):
    CHOICES: tuple[tuple[int, str], ...] = tuple(
        [(activity.id, activity.title) for activity in Activity.objects.all()]
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("choices", self.CHOICES)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.CHOICES
        return name, path, args, kwargs


class QuestionField(models.CharField):
    CHOICES = (
        ("char", "Short Text"),
        ("text", "Long Text"),
        ("datetime", "Date & Time"),
        ("bool", "True/False"),
        ("int", "Number"),
        ("email", "Email"),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("choices", self.CHOICES)
        kwargs.setdefault("max_length", 20)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.CHOICES
        return name, path, args, kwargs
