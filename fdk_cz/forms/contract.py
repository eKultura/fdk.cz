# FORMS.CONTRACT.PY


from django import forms
from fdk_cz.models import Contract

class contract_form(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['name', 'description', 'start_date', 'end_date', 'document']
