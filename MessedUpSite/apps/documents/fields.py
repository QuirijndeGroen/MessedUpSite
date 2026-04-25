from django.db import models


class DocumentTypeField(models.CharField):
    CHOICES = (
        ("gma", "GMA"),
        ("legal", "Legal"),
        ("other", "Other"),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 50)
        kwargs.setdefault("choices", self.CHOICES)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.CHOICES
        return name, path, args, kwargs


class DocumentLanguageField(models.CharField):
    CHOICES = (
        ("nl", "Dutch"),
        ("en", "English"),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 2)
        kwargs.setdefault("choices", self.CHOICES)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["choices"] = self.CHOICES
        return name, path, args, kwargs
