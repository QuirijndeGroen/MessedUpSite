"""User account views for the MessedUpSite application.

Provides views for user profiles, member management, content administration,
and CRUD operations for activities, documents, users, registration lists, and responses.
"""

from django.http import HttpRequest
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from MessedUpSite.apps.documents.models import Document
from MessedUpSite.apps.activities.models import Activity
from MessedUpSite.apps.registrationlists.models import RegistrationList, RegistrationResponses
from MessedUpSite.apps.activities.forms import ActivityForm
from MessedUpSite.apps.documents.forms import DocumentForm
from MessedUpSite.apps.registrationlists.forms import (
    RegistrationListForm,
    RegistrationListQuestionFormSet,
    RegistrationResponseForm,
)
from .models import Committee, User
from .forms import UserForm, CommitteeForm


# ============================================================================
# User Profile and Member Views
# ============================================================================


@login_required(login_url="/accounts/login/")
def ProfileView(request: HttpRequest):
    """Display the current user's profile and associated committees."""
    user = request.user
    committees = user.committees.values_list('name', flat=True)

    return render(request, "accounts/profile.html", {"user": user, "committees": committees})


@login_required(login_url="/accounts/login/")
def MembersView(request: HttpRequest):
    """Display active activities, tournaments, and documents for members."""
    try:
        activities = Activity.objects.filter(type="activity").order_by("start_time")
        activities = [activity for activity in activities if activity.is_active]
    except Activity.DoesNotExist:
        activities = None

    try:
        tournaments = Activity.objects.filter(type="tournament").order_by("start_time")
        tournaments = [tournament for tournament in tournaments if tournament.is_active]
    except Activity.DoesNotExist:
        tournaments = None

    try:
        documents = Document.objects.all().order_by("created")
    except Document.DoesNotExist:
        documents = None

    return render(
        request,
        "accounts/members.html",
        {
            "activities": activities,
            "tournaments": tournaments,
            "documents": documents,
        },
    )


# ============================================================================
# Content Management View
# ============================================================================


@login_required(login_url="/accounts/login/")
def AddContentView(request: HttpRequest):
    """Display content management dashboard with permission-based filtering.
    
    Renders different content based on user's committee permissions:
    - Full admin: all activities, documents, users, registration lists/responses
    - Committee-based: only content related to assigned committees
    """
    activities = "No access"
    documents = "No access"
    registration_lists = "No access"
    registration_responses = "No access"
    users = "No access"
    committees = "No access"

    user_rights = request.user.committees.values_list("rights", flat=True)

    if len(user_rights) > 0 or request.user.is_admin:
        # Check for Full admin rights
        
        if "Full" in user_rights or request.user.is_admin:
            activities = Activity.objects.all().order_by("start_time").prefetch_related(
                "registrationlists__questions"
            )
            documents = Document.objects.all().order_by("title")
            registration_lists = RegistrationList.objects.all().order_by("deadline")
            registration_responses = RegistrationResponses.objects.all().order_by("date_registered")
            users = User.objects.all().order_by("username")
            committees = Committee.objects.all().order_by("name")
        else:
            # Handle committee-based permissions
            committee_access = []
            has_document_access = False
            
            for committee_id, committee_rights in zip(request.user.committees.values_list('id', flat=True), user_rights):
                if "Documents & Activities" == committee_rights:
                    has_document_access = True
                    committee_access.append(committee_id)
                elif "Activity" == committee_rights:
                    committee_access.append(committee_id)
            
            # Filter based on accessible committees
            if committee_access:
                activities = Activity.objects.filter(organizer__in=committee_access).order_by("start_time").prefetch_related(
                    "registrationlists__questions"
                )
                registration_lists = RegistrationList.objects.filter(linked_activity__organizer__in=committee_access).order_by("deadline")
                registration_responses = RegistrationResponses.objects.filter(
                    linked_registrationlist__linked_activity__organizer__in=committee_access
                ).order_by("date_registered")
            
            # Documents only for Documents & Activities permission
            if has_document_access:
                documents = Document.objects.all().order_by("title")

    return render(
        request,
        "accounts/add_content.html",
        {
            "activities": activities,
            "documents": documents,
            "registration_lists": registration_lists,
            "registration_responses": registration_responses,
            "users": users,
            "committees": committees,            
        },
    )


# ============================================================================
# Activity Views (Add, Edit, Delete)
# ============================================================================


@login_required(login_url="/accounts/login/")
def ActivityAddView(request: HttpRequest):
    """Create a new activity. Requires activity permissions."""
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to add activities.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity added successfully!')
            return redirect('addcontent')
    else:
        form = ActivityForm()
    return render(request, 'accounts/activity_form.html', {'form': form, 'action': 'Add'})


@login_required(login_url="/accounts/login/")
def ActivityEditView(request: HttpRequest, pk: int):
    """Edit an existing activity. Requires activity permissions."""
    activity = get_object_or_404(Activity, pk=pk)
    
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to edit activities.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('addcontent')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'accounts/activity_form.html', {'form': form, 'action': 'Edit'})


@login_required(login_url="/accounts/login/")
def ActivityDeleteView(request: HttpRequest, pk: int):
    """Delete an activity. Requires activity permissions."""
    activity = get_object_or_404(Activity, pk=pk)
    
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to delete activities.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('addcontent')
    return render(request, 'accounts/confirm_delete.html', {'object': activity, 'object_type': 'Activity'})


# ============================================================================
# Document Views (Add, Edit, Delete)
# ============================================================================


@login_required(login_url="/accounts/login/")
def DocumentAddView(request: HttpRequest):
    """Create a new document. Requires document permissions."""
    # Check if user has document permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_document_permission = "Full" in user_rights or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_document_permission:
        messages.error(request, 'You do not have permission to add documents.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document added successfully!')
            return redirect('addcontent')
    else:
        form = DocumentForm()
    return render(request, 'accounts/document_form.html', {'form': form, 'action': 'Add'})


@login_required(login_url="/accounts/login/")
def DocumentEditView(request: HttpRequest, pk: int):
    """Edit an existing document. Requires document permissions."""
    document = get_object_or_404(Document, pk=pk)
    
    # Check if user has document permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_document_permission = "Full" in user_rights or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_document_permission:
        messages.error(request, 'You do not have permission to edit documents.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully!')
            return redirect('addcontent')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'accounts/document_form.html', {'form': form, 'action': 'Edit'})


@login_required(login_url="/accounts/login/")
def DocumentDeleteView(request: HttpRequest, pk: int):
    """Delete a document. Requires document permissions."""
    document = get_object_or_404(Document, pk=pk)
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_document_permission = "Full" in user_rights or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_document_permission:
        messages.error(request, 'You do not have permission to delete documents.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('addcontent')
    return render(request, 'accounts/confirm_delete.html', {'object': document, 'object_type': 'Document'})


# ============================================================================
# User Management Views (Add, Edit, Delete)
# ============================================================================


@login_required(login_url="/accounts/login/")
def UserAddView(request: HttpRequest):
    """Create a new user. Requires full admin permissions."""
    # Check if user has full admin permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_user_permission = "Full" in user_rights or request.user.is_admin
    
    if not has_user_permission:
        messages.error(request, 'You do not have permission to add users.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('addcontent')
    else:
        form = UserForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'action': 'Add'})


@login_required(login_url="/accounts/login/")
def UserEditView(request: HttpRequest, pk: int):
    """Edit an existing user. Requires full admin permissions."""
    user = get_object_or_404(User, pk=pk)
    
    # Check if user has full admin permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_user_permission = "Full" in user_rights or request.user.is_admin
    
    if not has_user_permission:
        messages.error(request, 'You do not have permission to edit users.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('addcontent')
    else:
        form = UserForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form, 'action': 'Edit'})


@login_required(login_url="/accounts/login/")
def UserDeleteView(request: HttpRequest, pk: int):
    """Delete a user. Requires full admin permissions."""
    user = get_object_or_404(User, pk=pk)
    
    # Check if user has full admin permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_user_permission = "Full" in user_rights or request.user.is_admin
    
    if not has_user_permission:
        messages.error(request, 'You do not have permission to delete users.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('addcontent')
    return render(request, 'accounts/confirm_delete.html', {'object': user, 'object_type': 'User'})


# ============================================================================
# Committee Management Views (Add, Edit, Delete)
# ============================================================================


@login_required(login_url="/accounts/login/")
def CommitteeAddView(request: HttpRequest):
    """Create a new committee. Requires full admin permissions."""
    # Check if user has full admin permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_user_permission = "Full" in user_rights or request.user.is_admin
    
    if not has_user_permission:
        messages.error(request, 'You do not have permission to add committees.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = CommitteeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Committee added successfully!')
            return redirect('addcontent')
    else:
        form = CommitteeForm()
    return render(request, 'accounts/committee_form.html', {'form': form, 'action': 'Add'})


@login_required(login_url="/accounts/login/")
def CommitteeEditView(request: HttpRequest, pk: int):
    """Edit an existing committee. Requires full admin permissions."""
    committee = get_object_or_404(Committee, pk=pk)
    
    # Check if user has full admin permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_user_permission = "Full" in user_rights or request.user.is_admin
    
    if not has_user_permission:
        messages.error(request, 'You do not have permission to edit committees.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = CommitteeForm(request.POST, instance=committee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Committee updated successfully!')
            return redirect('addcontent')
    else:
        form = CommitteeForm(instance=committee)
    return render(request, 'accounts/committee_form.html', {'form': form, 'action': 'Edit'})


@login_required(login_url="/accounts/login/")
def CommitteeDeleteView(request: HttpRequest, pk: int):
    """Delete a user. Requires full admin permissions."""
    committee = get_object_or_404(Committee, pk=pk)
    
    # Check if user has full admin permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_user_permission = "Full" in user_rights or request.user.is_admin
    
    if not has_user_permission:
        messages.error(request, 'You do not have permission to delete committees.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        committee.delete()
        messages.success(request, 'Committee deleted successfully!')
        return redirect('addcontent')
    return render(request, 'accounts/confirm_delete.html', {'object': committee, 'object_type': 'Committee'})


# ============================================================================
# Registration List Views (Add, Edit, Delete)
# ============================================================================


@login_required(login_url="/accounts/login/")
def RegistrationListAddView(request: HttpRequest):
    """Create a new registration list. Requires activity permissions."""
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to add registration lists.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = RegistrationListForm(request.POST)
        question_formset = RegistrationListQuestionFormSet(request.POST)
        if form.is_valid() and question_formset.is_valid():
            registration_list = form.save()
            question_formset.instance = registration_list
            question_formset.save()
            messages.success(request, 'Registration List added successfully!')
            return redirect('addcontent')
    else:
        form = RegistrationListForm()
        question_formset = RegistrationListQuestionFormSet()
    return render(
        request,
        'accounts/registrationlist_form.html',
        {'form': form, 'question_formset': question_formset, 'action': 'Add'},
    )


@login_required(login_url="/accounts/login/")
def RegistrationListEditView(request: HttpRequest, pk: int):
    """Edit an existing registration list. Requires activity permissions."""
    reg_list = get_object_or_404(RegistrationList, pk=pk)
    
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to edit registration lists.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = RegistrationListForm(request.POST, instance=reg_list)
        question_formset = RegistrationListQuestionFormSet(request.POST, instance=reg_list)
        if form.is_valid() and question_formset.is_valid():
            form.save()
            question_formset.save()
            messages.success(request, 'Registration List updated successfully!')
            return redirect('addcontent')
    else:
        form = RegistrationListForm(instance=reg_list)
        question_formset = RegistrationListQuestionFormSet(instance=reg_list)
    return render(
        request,
        'accounts/registrationlist_form.html',
        {'form': form, 'question_formset': question_formset, 'action': 'Edit'},
    )


@login_required(login_url="/accounts/login/")
def RegistrationListDeleteView(request: HttpRequest, pk: int):
    """Delete a registration list. Requires activity permissions."""
    reg_list = get_object_or_404(RegistrationList, pk=pk)
    
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to delete registration lists.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        reg_list.delete()
        messages.success(request, 'Registration List deleted successfully!')
        return redirect('addcontent')
    return render(request, 'accounts/confirm_delete.html', {'object': reg_list, 'object_type': 'Registration List'})


# ============================================================================
# Registration Response Views (Add, Edit, Delete)
# ============================================================================


@login_required(login_url="/accounts/login/")
def RegistrationResponseAddView(request: HttpRequest):
    """Create a new registration response. Requires activity permissions."""
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to add registration responses.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = RegistrationResponseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Response added successfully!')
            return redirect('addcontent')
    else:
        form = RegistrationResponseForm()
    return render(request, 'accounts/registrationresponse_form.html', {'form': form, 'action': 'Add'})


@login_required(login_url="/accounts/login/")
def RegistrationResponseEditView(request: HttpRequest, pk: int):
    """Edit an existing registration response. Requires activity permissions."""
    response = get_object_or_404(RegistrationResponses, pk=pk)
    
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to edit registration responses.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        form = RegistrationResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Response updated successfully!')
            return redirect('addcontent')
    else:
        form = RegistrationResponseForm(instance=response)
    return render(request, 'accounts/registrationresponse_form.html', {'form': form, 'action': 'Edit'})


@login_required(login_url="/accounts/login/")
def RegistrationResponseDeleteView(request: HttpRequest, pk: int):
    """Delete a registration response. Requires activity permissions."""
    response = get_object_or_404(RegistrationResponses, pk=pk)
    
    # Check if user has activity permissions
    user_rights = request.user.committees.values_list("rights", flat=True)
    has_activity_permission = "Full" in user_rights or any("Activity" in right for right in user_rights) or any("Documents & Activities" in right for right in user_rights) or request.user.is_admin
    
    if not has_activity_permission:
        messages.error(request, 'You do not have permission to delete registration responses.')
        return redirect('addcontent')
    
    if request.method == 'POST':
        response.delete()
        messages.success(request, 'Registration Response deleted successfully!')
        return redirect('addcontent')
    return render(request, 'accounts/confirm_delete.html', {'object': response, 'object_type': 'Registration Response'})
