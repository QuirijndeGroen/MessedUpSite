from django.db import models
from .fields import ActivityTypeField, OrganizerField


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
    organizer = (
        OrganizerField()
    )  # author = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created", "is_active"]

    def __str__(self):
        return self.title
