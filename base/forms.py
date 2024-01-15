from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms  import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
 

class MyUserCreationForm(UserCreationForm):
    
    error_messages = {
        'duplicate_username': 'This username is already taken. Please choose a different one.',
        'password_mismatch': 'The two password fields didn’t match.',
        'duplicate_email': 'This email is already associated with an account. Please use a different email.',
        'username_with_whitespace': 'Username should not contain white spaces.',
    }
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        if ' ' in username:
            raise forms.ValidationError(
                self.error_messages['username_with_whitespace'],
                code='username_with_whitespace',
            )
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
            )
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email',
            )
        except User.DoesNotExist:
            return email






class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host',  'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email','bio']