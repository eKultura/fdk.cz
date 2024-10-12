# FORMS.ACCOUNTING.PY

from datetime import datetime, timedelta
from decimal import Decimal
from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.utils import timezone

from fdk_cz.models import invoice, invoice_item


class FreeInvoiceForm(forms.Form):
    # Informace o dodavateli
    company_name = forms.CharField(label='Název firmy / jméno', max_length=255)
    street = forms.CharField(label='Ulice', max_length=255)
    street_number = forms.CharField(label='Číslo popisné', max_length=20)
    city = forms.CharField(label='Město', max_length=255)
    postal_code = forms.CharField(label='PSČ', max_length=20)
    ico = forms.CharField(label='IČO', max_length=20)
    dic = forms.CharField(label='DIČ', max_length=20, required=False)

    # Přidaná pole pro údaje o odběrateli
    client_name = forms.CharField(label='Název firmy / jméno odběratele', max_length=255)
    client_street = forms.CharField(label='Ulice odběratele', max_length=255)
    client_street_number = forms.CharField(label='Číslo popisné odběratele', max_length=20)
    client_city = forms.CharField(label='Město odběratele', max_length=255)
    client_postal_code = forms.CharField(label='PSČ odběratele', max_length=20)
    client_ico = forms.CharField(label='IČO odběratele', max_length=20, required=False)
    client_dic = forms.CharField(label='DIČ odběratele', max_length=20, required=False)

    # Přidání polí pro číslo účtu a kód banky
    account_number = forms.CharField(label='Číslo účtu', max_length=20)
    bank_code = forms.CharField(label='Kód banky', max_length=4)

    # Informace o faktuře
    issue_date = forms.DateField(
        label='Datum vystavení',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=datetime.today().strftime('%Y-%m-%d')
    )
    due_date = forms.DateField(
        label='Datum splatnosti',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=(datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    )
    is_vat_payer = forms.BooleanField(label="Jsem plátce DPH", required=False)


    vat_rate = forms.DecimalField(label='DPH (%)', max_digits=5, decimal_places=2, initial=21)
    without_vat = forms.BooleanField(label='Nejsem plátce DPH', required=False)
    payment_method = forms.ChoiceField(
        label='Způsob úhrady',
        choices=[('bank', 'Převod na účet'), ('cash', 'Hotově')]
    )




class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = invoice_item
        fields = ['description', 'quantity', 'unit_price', 'total_price']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Popis položky'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Množství', 'value': 1}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena za jednotku'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Celková cena'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')

        if quantity and unit_price:
            cleaned_data['total_price'] = quantity * unit_price
        return cleaned_data

# Formset pro více položek
InvoiceItemFormSet = modelformset_factory(
    invoice_item,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True
)





class InvoiceForm(forms.ModelForm):
    is_vat_payer = forms.BooleanField(required=False, label="Jsem plátce DPH")

    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date(),
        label="Datum vystavení"
    )
    
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Datum splatnosti"
    )

    vat_rate = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,  # Standardně není povinné
        label="DPH (%)",
        min_value=0,
        initial=21  # Výchozí hodnota je 21 %
    )

    class Meta:
        model = invoice
        fields = ['issue_date', 'due_date', 'vat_rate', 'is_vat_payer', 'is_paid']

        def clean(self):
            cleaned_data = super().clean()
            is_vat_payer = cleaned_data.get('is_vat_payer', False)
            
            # Pokud není uživatel plátcem DPH, vymaž hodnotu DPH
            if not is_vat_payer:
                cleaned_data['vat_rate'] = None
            elif is_vat_payer and not cleaned_data.get('vat_rate'):
                # Uživatel je plátcem, ale nevyplnil DPH
                self.add_error('vat_rate', 'Toto pole je třeba vyplnit.')
                
            return cleaned_data





"""
class InvoiceItemForm(forms.ModelForm):
    quantity = forms.DecimalField(
        initial=1,  
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Množství'})
    )
    
    unit_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena za jednotku'})
    )
    
    total_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Celková cena'})
    )

    class Meta:
        model = invoice_item
        fields = ['description', 'quantity', 'unit_price', 'total_price']

    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Popis položky'})


InvoiceItemFormSet = modelformset_factory(
    invoice_item,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True 
)
"""