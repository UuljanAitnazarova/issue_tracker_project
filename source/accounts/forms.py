from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from accounts.models import Profile
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



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Old password", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Old password is incorrect!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']




