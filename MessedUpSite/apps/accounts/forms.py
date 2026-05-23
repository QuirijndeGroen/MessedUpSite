from django import forms
from .models import User, Committee
from .fields import CommitteeRightsField


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Leave blank to keep the current password.'
    )
    committees = forms.ModelMultipleChoiceField(
        queryset=Committee.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'committees', 'is_admin', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user


class CommitteeForm(forms.ModelForm):
    rights = forms.ChoiceField(
        choices=CommitteeRightsField.CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = Committee
        fields = ['name', 'rights']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Committee Name'}),
        }