from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class SignUpForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text'}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Enter email', 'name': 'email', }))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'name': 'password'}))


class ServiceDemandForm(forms.ModelForm):
    # Fields from ServiceDemand model
    service_type = forms.ModelChoiceField(queryset=ServiceDemand.objects.all())
    object = forms.CharField()
    details = forms.CharField(widget=forms.Textarea)

    # Fields from Client model
    address = forms.CharField()
    country = forms.CharField()
    phone = forms.CharField()

    class Meta:
        model = ServiceDemand
        fields = ['service_type', 'object', 'details', 'address', 'country', 'phone']

class RejectionReason(forms.ModelForm):
    reason = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Enter the reason', 'name': 'reason', }))
