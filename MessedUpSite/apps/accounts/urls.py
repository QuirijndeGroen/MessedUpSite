from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from MessedUpSite.apps.quotes.views import newquote

name = "accounts"
urlpatterns = [
    path("profile/", views.ProfileView, name="profile"),
    path("members/", views.MembersView, name="members"),
    path("newquote/", newquote, name="newquote"),
    path("addcontent/", views.AddContentView, name="addcontent"),
    # Activity URLs
    path("activity/add/", views.ActivityAddView, name="activity-add"),
    path("activity/<int:pk>/edit/", views.ActivityEditView, name="activity-edit"),
    path("activity/<int:pk>/delete/", views.ActivityDeleteView, name="activity-delete"),
    # Document URLs
    path("document/add/", views.DocumentAddView, name="document-add"),
    path("document/<int:pk>/edit/", views.DocumentEditView, name="document-edit"),
    path("document/<int:pk>/delete/", views.DocumentDeleteView, name="document-delete"),
    # User URLs
    path("user/add/", views.UserAddView, name="user-add"),
    path("user/<int:pk>/edit/", views.UserEditView, name="user-edit"),
    path("user/<int:pk>/delete/", views.UserDeleteView, name="user-delete"),
    # Committee URLs
    path("committee/add/", views.CommitteeAddView, name="committee-add"),
    path("committee/<int:pk>/edit/", views.CommitteeEditView, name="committee-edit"),
    path(
        "committee/<int:pk>/delete/", views.CommitteeDeleteView, name="committee-delete"
    ),
    # Registration List URLs
    path(
        "registrationlist/add/",
        views.RegistrationListAddView,
        name="registrationlist-add",
    ),
    path(
        "registrationlist/<int:pk>/edit/",
        views.RegistrationListEditView,
        name="registrationlist-edit",
    ),
    path(
        "registrationlist/<int:pk>/delete/",
        views.RegistrationListDeleteView,
        name="registrationlist-delete",
    ),
    # Registration Response URLs
    path(
        "registrationresponse/add/<int:registrationlist_pk>/",
        views.RegistrationResponseAddView,
        name="registrationresponse-add",
    ),
    path(
        "registrationresponse/<int:pk>/edit/",
        views.RegistrationResponseEditView,
        name="registrationresponse-edit",
    ),
    path(
        "registrationresponse/<int:pk>/delete/",
        views.RegistrationResponseDeleteView,
        name="registrationresponse-delete",
    ),
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
