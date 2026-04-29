from django import forms

class RegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions", [])
        super().__init__(*args, **kwargs)

        for question in questions:
            field_name = f"question_{question.id}"
            label = question.question
            required = question.mandatory

            if question.type == "char":
                self.fields[field_name] = forms.CharField(label=label, required=required, max_length=255, widget=forms.TextInput(attrs={'class': 'input-container awnser-field'}))
            elif question.type == "text":
                self.fields[field_name] = forms.CharField(label=label, required=required, widget=forms.Textarea(attrs={'class': 'input-container awnser-field'})) 
            elif question.type == "datetime":
                self.fields[field_name] = forms.DateTimeField(
                    label=label,
                    required=required,
                    widget=forms.DateTimeInput(attrs={"type": "datetime-local", 'class': 'input-container awnser-field'}),
                )
            elif question.type == "bool":
                self.fields[field_name] = forms.BooleanField(label=label, required=required, widget=forms.CheckboxInput(attrs={'class': 'input-container awnser-field'}))
            elif question.type == "int":
                self.fields[field_name] = forms.IntegerField(label=label, required=required, widget=forms.NumberInput(attrs={'class': 'input-container awnser-field'}))
            elif question.type == "email":
                self.fields[field_name] = forms.EmailField(label=label, required=required, widget=forms.EmailInput(attrs={'class': 'input-container awnser-field'}))