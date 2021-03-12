from django import forms

from .models import Issue, Type, Status


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status','type']
