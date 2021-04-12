from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Issue, Type, Status, Project


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'type']


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Search')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']


class MyUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=30, required=True)
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        super(MyUserCreationForm, self).clean()
        if not self.cleaned_data.get('first_name') or self.cleaned_data.get('last_name'):
            raise ValidationError('First name or last name should be registered.')

