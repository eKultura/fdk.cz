# forms.user.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from fdk_cz.models import UserProfile

class profile_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class user_contact_form(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'location','photo']
        widgets = { 'phone_number' : forms.TextInput(attrs={'class': 'form-control'}),
          'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class user_registration_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        return password

    def save(self, commit=True):
        user = super(user_registration_form, self).save(commit=False)
        user.email = self.cleaned_data['email']
     
        user.password = self.cleaned_data['password'] 

        if commit:
            user.save()
        return user



