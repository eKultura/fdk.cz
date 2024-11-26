from django import forms
from fdk_cz.models import transaction, warehouse

class transaction_form(forms.ModelForm):
    class Meta:
        model = transaction
        fields = ['transaction_type', 'quantity']
        labels = {
            'transaction_type': 'Typ transakce',
            'quantity': 'Částka',
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Zadejte částku'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Popis transakce'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Vyberte typ transakce"

# Příklad dalších formulářů pro sklad a další operace
