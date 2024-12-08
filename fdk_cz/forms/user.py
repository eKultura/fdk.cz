# forms.user.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class profile_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class password_renewal_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
    

class reset_password_form(forms.Form):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        max_length=128,
    )
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1:  # Only validate if password1 is provided
            try:
                validate_password(password1)  # Django's built-in password validators
            except ValidationError as e:
                raise forms.ValidationError(e.messages)  # Display validation errors in the form
        return password1

class user_registration_form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super(user_registration_form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



