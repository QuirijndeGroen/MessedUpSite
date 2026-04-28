from django.db import models
from .fields import QuestionField


class RegistrationList(models.Model):
    """Represents an activity that users can participate in."""

    created = models.DateTimeField(auto_now_add=True)
    linked_activity = models.ForeignKey(
        "activities.Activity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        activity = self.linked_activity
        if activity is None:
            return "Unlinked Registration List"
        return f"{activity.title} Registration List"


class Question(models.Model):
    registration_list = models.ForeignKey(
        RegistrationList, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=255)
    type = QuestionField()
    mandatory = models.BooleanField(default=False)

    def __str__(self):
        return self.question
