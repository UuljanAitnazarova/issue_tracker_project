from django import forms

from .models import Issue, Type, Status


class IssueForm(forms.ModelForm):
    class Meta:
        type = forms.ModelChoiceField(queryset=Type.objects.all())
        model = Issue
        fields = ['summary', 'description', 'type', 'status']
