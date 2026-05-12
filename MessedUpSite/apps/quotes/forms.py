from django import forms

from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'person']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter the quote here...',
            }),
            'person': forms.TextInput(attrs={
                'placeholder': 'Enter the person here...',
            }),
        }
        labels = {
            'text': 'Quote',
            'person': 'Person',
        }