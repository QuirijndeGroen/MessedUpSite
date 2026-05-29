from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["type", "language", "title", "file", "priority"]
        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Document Title"}
            ),
            "file": forms.FileInput(attrs={"class": "form-control"}),
            "priority": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Priority"}
            ),
        }
