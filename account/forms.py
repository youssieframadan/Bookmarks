from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from django.core.exceptions import ValidationError
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="username or email")
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already Exists.')
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth','photo')

