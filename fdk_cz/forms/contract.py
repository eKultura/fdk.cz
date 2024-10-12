# FORMS.CONTRACT.PY


from django import forms
from fdk_cz.models import contract

class contract_form(forms.ModelForm):
    class Meta:
        model = contract
        fields = ['name', 'description', 'start_date', 'end_date', 'document']
