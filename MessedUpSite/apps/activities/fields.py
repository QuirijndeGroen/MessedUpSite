from django.db import models


class ActivityTypeField(models.CharField):
    CHOICES = (
        ("activity", "Activity"),
        ("tournament", "Tournament"),
        ("poll", "Poll"),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 50)
        kwargs.setdefault("choices", self.CHOICES)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.CHOICES
        return name, path, args, kwargs
