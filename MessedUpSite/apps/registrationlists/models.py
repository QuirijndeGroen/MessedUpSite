from django.db import models
from .fields import ActivityField, QuestionField
from MessedUpSite.apps.activities.models import Activity


class RegistrationList(models.Model):
    """Represents an activity that users can participate in."""

    created = models.DateTimeField(auto_now_add=True)
    linked_activity = ActivityField()
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return (
            Activity.objects.get(id=self.linked_activity).title + " Registration List"
        )


class Question(models.Model):
    registration_list = models.ForeignKey(
        RegistrationList, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=255)
    type = QuestionField()
    mandatory = models.BooleanField(default=False)

    def __str__(self):
        return self.question
