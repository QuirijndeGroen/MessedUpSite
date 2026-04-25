from django.db import models
from .fields import DocumentLanguageField, DocumentTypeField


class Document(models.Model):
    """Represents a document."""

    created = models.DateTimeField(auto_now_add=True)
    type = DocumentTypeField(default="other")
    language = DocumentLanguageField(default="en")
    title = models.CharField(max_length=100, blank=True, default="", unique=True)
    file = models.FileField(upload_to="MessedUpSite/static/documents")
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.title
