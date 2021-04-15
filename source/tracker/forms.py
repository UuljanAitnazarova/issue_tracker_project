from django import forms
from django.contrib.auth.models import User

from .models import Issue, Project


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



