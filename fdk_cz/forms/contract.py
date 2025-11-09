# FORMS.CONTRACT.PY


from django import forms
from fdk_cz.models import Contract

class contract_form(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['name', 'description', 'start_date', 'end_date', 'document']

        # Tailwind CSS styling
        tw_input = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'

        widgets = {
            'name': forms.TextInput(attrs={'class': tw_input, 'placeholder': 'Název smlouvy'}),
            'description': forms.Textarea(attrs={'class': tw_input, 'rows': 4, 'placeholder': 'Popis smlouvy'}),
            'start_date': forms.DateInput(attrs={'class': tw_input, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': tw_input, 'type': 'date'}),
            'document': forms.FileInput(attrs={'class': tw_input}),
        }
