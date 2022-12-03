from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Task

class UserCreationForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['task_name']
		widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type here..'}),
        }

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']