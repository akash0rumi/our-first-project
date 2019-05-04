from django import forms
from .models import user_profile_info
from django.contrib.auth.models import User

class user_form(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class user_profile_info_form(forms.ModelForm):
    class Meta():
        model = user_profile_info
        fields = ('profolio_site', 'profile_pic')
