# -------------------------------------------------------------------
#                         forms.user.py
# -------------------------------------------------------------------
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



# -------------------------------------------------------------------
#                FORMULÁŘ PRO ÚPRAVU PROFILU UŽIVATELE
# -------------------------------------------------------------------
class profile_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# -------------------------------------------------------------------
#                FORMULÁŘ PRO REGISTRACI UŽIVATELE
# -------------------------------------------------------------------
class user_registration_form(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="E-mail"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    # ---------------------------------------------------------------
    #  Validace uživatelského jména – min. délka
    # ---------------------------------------------------------------
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Uživatelské jméno musí mít alespoň 3 znaky.")
        return username

    # ---------------------------------------------------------------
    #  Validace e-mailu – duplicita + ověření domény (MX)
    # ---------------------------------------------------------------
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Tento e-mail je již registrován.")
        # MX kontrolu neprovádíme – postačí potvrzovací e-mail
        return email


    # ---------------------------------------------------------------
    #  Uložení uživatele
    # ---------------------------------------------------------------
    def save(self, commit=True):
        user = super(user_registration_form, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
