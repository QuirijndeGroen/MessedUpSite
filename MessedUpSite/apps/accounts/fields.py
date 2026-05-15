from django.db import models
from django.contrib.postgres.fields import ArrayField


class CommitteeField(models.CharField):
    CHOICES = (
        ("Board", "Board"),
        ("Technical Committee", "Technical Committee"),
        ("Promo", "Promo"),
        ("Kascommittee", "Kascommittee"),
        ("Board of Advice", "Board of Advice"),
        ("Bar Committee", "Bar Committee"),
        ("ISSTT Committee", "ISSTT Committee"),
        ("Webcommittee", "Webcommittee"),
        ("First-year Committee", "First-year Committee"),
        ("Weekend Committee", "Weekend Committee"),
    )

    choices = ArrayField(
        models.CharField(max_length=10, choices=CHOICES, blank=True, default=list)
    )
