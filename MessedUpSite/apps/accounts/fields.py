from django.db import models


class CommitteeRightsField(models.CharField):
    CHOICES = (
        ("Full", "Has full access to all documents and all activities"),
        ("Activity", "Can add and manage activities of the committee"),
        ("Documents & Activities", "Can add documents and add or manage activities of the committee"),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 50)
        kwargs.setdefault("choices", self.CHOICES)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.CHOICES
        return name, path, args, kwargs