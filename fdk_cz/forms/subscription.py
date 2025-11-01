# fdk_cz/forms/subscription.py

from django import forms
from fdk_cz.models import UserModuleSubscription


class SubscriptionForm(forms.ModelForm):
    """Formulář pro výběr typu předplatného"""

    class Meta:
        model = UserModuleSubscription
        fields = ['subscription_type']
        widgets = {
            'subscription_type': forms.RadioSelect()
        }


class CancellationForm(forms.Form):
    """Formulář pro zrušení předplatného"""

    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Proč rušíte předplatné? (volitelné)',
            'class': 'form-control'
        }),
        required=False,
        label='Důvod zrušení'
    )
