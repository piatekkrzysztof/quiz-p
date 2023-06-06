from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from quizp.models import *

class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email=forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Different passwords!")

    def clean_login(self):
        user_name = self.cleaned_data.get('login')
        user = User.objects.filter(username=user_name)
        if user:
            raise ValidationError("Username already taken!")
        return user_name
