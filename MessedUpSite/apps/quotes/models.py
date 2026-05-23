from django.db import models
from MessedUpSite.apps.accounts.models import User

# Create your models here.
class Quote(models.Model):
    """Represents an quote said by someone."""

    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    person = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'"{self.text}" - {self.person}'
    