from django import forms
from django.contrib.auth.forms import AuthenticationForm
from.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('name', 'email')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')