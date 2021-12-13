# users/forms.py
from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField
from django.contrib.auth.forms import UserCreationForm
from .models import UserTimer, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)



class UserUpdateForm(ModelForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(ModelForm):
    class Meta: 
        model = Profile
        fields = '__all__'


class DashboardUpdateForm(ModelForm):
    class Meta: 
        model = UserTimer
        fields = ['timers', 'display_order']