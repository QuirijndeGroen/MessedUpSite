from django.db import models


class Document(models.Model):
    """Represents a document."""

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to="MessedUpSite/static/documents")
    type = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.title
