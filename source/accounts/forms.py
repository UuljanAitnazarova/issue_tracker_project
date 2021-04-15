from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from tracker.models import Project


class ProjectUserForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['user']
        widgets = {'user':CheckboxSelectMultiple}


class MyUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=30, required=True)
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        super(MyUserCreationForm, self).clean()
        if not self.cleaned_data.get('first_name') and not self.cleaned_data.get('last_name'):
            raise ValidationError('First name or last name should be registered.')
