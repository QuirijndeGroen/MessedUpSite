from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .models import Quote
from .forms import QuoteForm

# Create your views here.
@login_required(login_url="/accounts/login/")
def newquote(request: HttpRequest):

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.author = request.user
            quote.save()
            messages.success(request, "Quote submitted successfully!")
            return redirect("quotes:quote_list")
    else:
        form = QuoteForm()

    return render(request, "accounts/newquote.html", {
        "form": form
    })


def quote_list(request: HttpRequest):

    quotes = Quote.objects.all().order_by("-created") 

    return render(request, "accounts/quotes.html", {
        "quotes": quotes
    })