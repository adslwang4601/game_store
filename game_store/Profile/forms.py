from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from .models import User_Profile
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=("Enter the same password as above, for verification."))
    applyAsDeveloper = forms.NullBooleanField(label="Apply as Developer", widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ['date_of_birth', 'photo', 'city', 'country']

