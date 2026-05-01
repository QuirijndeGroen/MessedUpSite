from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm
from .models import RegistrationAnswer, RegistrationList, RegistrationResponses


@login_required(login_url="/accounts/login/")
def submit_registration(request, pk):
    registrationlist = get_object_or_404(RegistrationList, pk=pk)
    questions = registrationlist.questions.all()

    if request.method != "POST":
        return redirect("activities")

    form = RegistrationForm(request.POST, questions=questions)
    if not form.is_valid():
        messages.error(request, "Please correct the registration form and submit again.")
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

    messages.success(request, "Your registration was submitted successfully.")
    return redirect("activities")


@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def deregister(request, pk):
    """Handle user deregistration from a registration list."""
    registrationlist = get_object_or_404(RegistrationList, pk=pk)
    
    # Find the user's registration
    registration = RegistrationResponses.objects.filter(
        linked_registrationlist=registrationlist,
        user=request.user
    ).first()
    
    if registration is None:
        return JsonResponse({
            'success': False,
            'message': 'You are not registered for this activity.'
        }, status=400)
    
    # Delete the registration and all associated answers
    registration.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'You have been successfully deregistered from this activity.'
    })


@login_required(login_url="/accounts/login/")
def view_responses(request, pk):
    registrationlist = get_object_or_404(RegistrationList, pk=pk)
    
    # Get all responses with their answers
    responses = registrationlist.responses.select_related('user').prefetch_related('answers__question').all()
    
    # Get all questions for the header
    questions = list(registrationlist.questions.order_by('id'))
    
    # Create a matrix: user -> question -> answer
    response_data = []
    for response in responses:
        # Create a dictionary of question_id -> answer
        user_answers = {answer.question_id: answer.answer for answer in response.answers.all()}
        
        # Create a list of answers in the same order as questions
        answers_list = []
        for question in questions:
            answers_list.append(user_answers.get(question.id, "-"))
        
        response_data.append({
            'user': response.user,
            'date_registered': response.date_registered,
            'answers': answers_list  # Now a list instead of dict
        })
    
    context = {
        'registrationlist': registrationlist,
        'questions': questions,
        'response_data': response_data,
    }
    
    return render(request, 'accounts/registration_responses.html', context)
