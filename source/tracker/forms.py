from django import forms

from .models import Issue, Type, Status


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status','type']


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Search')