from django import forms
from .models import CustomUser, Todolist, TodolistItem
from django.contrib.auth.forms import UserCreationForm


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class TodolistCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'description', 'deadline']
        widgets = {'deadline': forms.DateInput(attrs={'type': 'date'})}