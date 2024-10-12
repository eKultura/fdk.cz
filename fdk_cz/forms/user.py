# forms.user.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class user_registration_form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(user_registration_form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



