from django.contrib import admin
from .models import (
    Question,
    RegistrationAnswer,
    RegistrationList,
    RegistrationResponses,
)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class RegistrationAnswerInline(admin.TabularInline):
    model = RegistrationAnswer
    extra = 0
    readonly_fields = ["question", "answer"]


@admin.register(RegistrationList)
class RegistrationListAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


@admin.register(RegistrationResponses)
class RegistrationResponsesAdmin(admin.ModelAdmin):
    list_display = ["linked_registrationlist", "date_registered", "user"]
    inlines = [RegistrationAnswerInline]
