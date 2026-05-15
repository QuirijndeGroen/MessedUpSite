from django.http import HttpRequest

from .models import Quote


def random_quote(request: HttpRequest):
    """Inject a random quote into every template context."""
    try:
        quote = Quote.objects.order_by("?").first()
    except Quote.DoesNotExist:
        quote = None
    
    return {"quote": quote}