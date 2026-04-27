from django.contrib import admin
from .models import RegistrationList, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(RegistrationList)
class RegistrationListAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
