from django.db import models


class ActivityField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("choices", [])
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_activity_choices():
        from MessedUpSite.apps.activities.models import Activity

        return [(activity.id, activity.title) for activity in Activity.objects.all()]

    def formfield(self, **kwargs):
        defaults = {"choices": self.get_activity_choices()}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("choices", None)
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
