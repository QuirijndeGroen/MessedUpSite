from django.http import HttpRequest

from .models import Quote


def random_quote(request: HttpRequest):
    """Inject a random quote into every template context."""
    quote = Quote.objects.order_by("?").first()
    return {"quote": quote}
