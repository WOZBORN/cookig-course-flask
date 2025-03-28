from django import forms
from .models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['fullname', 'email', 'phone']
        labels = {
            'fullname': 'ФИО',
            'email': 'Email',
            'phone': 'Телефон',
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
