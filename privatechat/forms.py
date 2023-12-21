from django import forms
from .models import PrivateMessage   

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['body']   
