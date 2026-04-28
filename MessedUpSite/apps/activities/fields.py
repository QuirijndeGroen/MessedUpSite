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


class OrganizerField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 50)
        kwargs.setdefault("choices", [])
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_persona_choices():
        from MessedUpSite.apps.accounts.models import UserPersona

        return [
            (persona.normalized_name, persona.name)
            for persona in UserPersona.objects.all()
        ]

    def formfield(self, **kwargs):
        defaults = {
            "choices": self.get_persona_choices(),
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("choices", None)
        return name, path, args, kwargs
