from django.db import DatabaseError
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from .models import Quote


def random_quote(request: HttpRequest):
    """Inject a random quote into every template context."""
    if request.user:
        try:
            quote = Quote.objects.order_by("?").first()
        except Quote.DoesNotExist:
            quote = None
    else:
        quote = None

    return {"quote": quote}
