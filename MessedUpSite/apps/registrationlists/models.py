from django.db import models
from .fields import QuestionField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class RegistrationList(models.Model):
    """Represents an activity that users can participate in."""

    created = models.DateTimeField(auto_now_add=True)
    linked_activity = models.ForeignKey(
        "activities.Activity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrationlists",
    )
    description = models.TextField()
    deadline = models.DateTimeField()
    registrations_public = models.BooleanField(default=True)

    @property
    def closed(self):
        return date.today() > self.deadline.date()

    def __str__(self):
        activity = self.linked_activity
        if activity is None:
            return "Unlinked Registration List"
        self.title = f"{activity.title} Registration List"
        return self.title


class Question(models.Model):
    registration_list = models.ForeignKey(
        RegistrationList, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=255)
    type = QuestionField()
    mandatory = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class RegistrationResponses(models.Model):

    linked_registrationlist = models.ForeignKey(
        "registrationlists.RegistrationList",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responses",
    )
    date_registered = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        registrationlist = self.linked_registrationlist
        if registrationlist is None:
            return "Unlinked Registration List"
        return f"{registrationlist.__str__()} Responses"


class RegistrationAnswer(models.Model):
    response = models.ForeignKey(
        RegistrationResponses,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    answer = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("response", "question")

    def __str__(self):
        return f"Answer to '{self.question}'"
