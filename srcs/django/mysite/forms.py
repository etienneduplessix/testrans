from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Person
from django import forms


class NameForm(forms.Form):
	your_name = forms.CharField(label="Your name", max_length=100)