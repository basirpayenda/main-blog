from django import forms
from .models import Signup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email',
        'name': 'email',
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'Type your email address'
    }), label='')

    class Meta:
        model = Signup
        fields = ('email',)
