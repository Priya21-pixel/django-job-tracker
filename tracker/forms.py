from django import forms
from .models import Job
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company', 'position', 'link', 'date_applied', 'deadline', 'status']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
