from django import forms

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

