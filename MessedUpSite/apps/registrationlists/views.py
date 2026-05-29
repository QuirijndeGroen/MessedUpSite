from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm
from .models import RegistrationAnswer, RegistrationList, RegistrationResponses


def submit_registration(request: HttpRequest, pk: int):
    registrationlist = get_object_or_404(RegistrationList, pk=pk)
    questions = registrationlist.questions.all()

    if request.method != "POST":
        return redirect("activities")

    form = RegistrationForm(request.POST, questions=questions)
    if not form.is_valid():
        error_msg = "Please correct the registration form and submit again."
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "message": error_msg}, status=400)
        messages.error(request, error_msg)
        return redirect("activities")

    if registrationlist.registrations_public:
        response = RegistrationResponses.objects.create(
            linked_registrationlist=registrationlist,
            user=request.user if request.user.is_authenticated else None,
        )
    else:
        if not request.user.is_authenticated:
            error_msg = "You must be logged in to register for this activity."
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {"success": False, "message": error_msg}, status=403
                )
            messages.error(request, error_msg)
            return redirect("activities")

        response = RegistrationResponses.objects.create(
            linked_registrationlist=registrationlist,
            user=request.user,
        )

    for question in questions:
        field_name = f"question_{question.id}"
        raw_answer = form.cleaned_data.get(field_name)

        if raw_answer is None:
            answer_text = "-"
        elif isinstance(raw_answer, bool):
            answer_text = str(raw_answer)
        elif hasattr(raw_answer, "isoformat"):
            answer_text = raw_answer.isoformat()
        else:
            answer_text = str(raw_answer)

        RegistrationAnswer.objects.create(
            response=response,
            question=question,
            answer=answer_text,
        )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "message": "Your registration was submitted successfully.",
            }
        )

    messages.success(request, "Your registration was submitted successfully.")
    return redirect("activities")


@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def deregister(request: HttpRequest, pk: int):
    """Handle user deregistration from a registration list."""
    registrationlist = get_object_or_404(RegistrationList, pk=pk)

    # Find the user's registration
    registration = RegistrationResponses.objects.filter(
        linked_registrationlist=registrationlist, user=request.user
    ).first()

    if registration is None:
        return JsonResponse(
            {"success": False, "message": "You are not registered for this activity."},
            status=400,
        )

    # Delete the registration and all associated answers
    registration.delete()

    return JsonResponse(
        {
            "success": True,
            "message": "You have been successfully deregistered from this activity.",
        }
    )


@login_required(login_url="/accounts/login/")
def view_responses(request: HttpRequest, pk: int):
    registrationlist = get_object_or_404(RegistrationList, pk=pk)

    can_add_responses = False
    response_list = []

    try:
        organizer = registrationlist.linked_activity.organizer
    except AttributeError:
        organizer = None

    can_add_responses = (
        request.user.is_admin
        or request.user.committees.filter(name="Board").exists()
        or (
            organizer is not None
            and organizer.id in request.user.committees.values_list("id", flat=True)
        )
    )

    if can_add_responses:
        # Get all responses with their answers
        responses_table = (
            registrationlist.responses.select_related("user")
            .prefetch_related("answers__question")
            .all()
        )
    else:
        # Get the response from the user with their answers
        responses_table = (
            registrationlist.responses.select_related("user")
            .prefetch_related("answers__question")
            .filter(user=request.user)
        )

        if registrationlist.registrations_public:
            responses_list = registrationlist.responses.all()

            for response in responses_list:
                response_list.append(
                    {
                        "user": response.user,
                        "date_registered": response.date_registered,
                    }
                )

    # Get all questions for the header
    questions = list(registrationlist.questions.order_by("id"))

    # Create a matrix: user -> question -> answer
    response_table = []
    for response in responses_table:
        # Create a dictionary of question_id -> answer
        user_answers = {
            answer.question_id: answer.answer for answer in response.answers.all()
        }

        # Create a list of answers in the same order as questions
        answers_list = []
        for question in questions:
            answers_list.append(user_answers.get(question.id, "-"))

        response_table.append(
            {
                "pk": response.pk,
                "user": response.user,
                "date_registered": response.date_registered,
                "answers": answers_list,  # Now a list instead of dict
            }
        )

    context = {
        "registrationlist": registrationlist,
        "questions": questions,
        "response_table": response_table,
        "response_list": response_list,
        "can_add_responses": can_add_responses,
    }

    return render(request, "accounts/registration_responses.html", context)
