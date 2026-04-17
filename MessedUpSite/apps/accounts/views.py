from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def ProfileView(request):
    return TemplateView.as_view(template_name="accounts/profile.html")(request)


@login_required(login_url="/accounts/login/")
def MembersView(request):
    return TemplateView.as_view(template_name="accounts/members.html")(request)
