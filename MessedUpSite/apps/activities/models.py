from datetime import date

from django.db import models
from .fields import ActivityTypeField


class Activity(models.Model):
    """Represents an activity that users can participate in."""

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    type = ActivityTypeField()
    image = models.ImageField(
        blank=True,
        default="/MessedUpSite/static/assets/Images/Logo Light.png",
        upload_to="MessedUpSite/static/activity_images",
    )
    title = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(
        "accounts.Committee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organizer",
    )
    public=models.BooleanField(default=False)

    @property
    def is_active(self):
        return date.today() <= self.end_time.date()

    class Meta:
        ordering = ["start_time"]
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title
