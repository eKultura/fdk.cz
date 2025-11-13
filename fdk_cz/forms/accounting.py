# FORMS.ACCOUNTING.PY

from datetime import datetime, timedelta
from decimal import Decimal
from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.utils import timezone

from fdk_cz.models import (
    Invoice, InvoiceItem,
    AccountingContext, AccountingAccount, JournalEntry, JournalEntryLine, BalanceSheet,
    Organization
)


class FreeInvoiceForm(forms.Form):
    # Informace o dodavateli
    company_name = forms.CharField(label='Název firmy / jméno', max_length=255)
    street = forms.CharField(label='Ulice', max_length=255, required=False)
    street_number = forms.CharField(label='Číslo popisné', max_length=20, required=False)
    city = forms.CharField(label='Město', max_length=255, required=False)
    postal_code = forms.CharField(label='PSČ', max_length=20, required=False)
    ico = forms.CharField(label='IČO', max_length=20, required=False)
    dic = forms.CharField(label='DIČ', max_length=20, required=False)

    # Přidaná pole pro údaje o odběrateli
    client_name = forms.CharField(label='Název firmy / jméno odběratele', max_length=255)
    client_street = forms.CharField(label='Ulice odběratele', max_length=255, required=False)
    client_street_number = forms.CharField(label='Číslo popisné odběratele', max_length=20, required=False)
    client_city = forms.CharField(label='Město odběratele', max_length=255, required=False)
    client_postal_code = forms.CharField(label='PSČ odběratele', max_length=20, required=False)
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
        model = InvoiceItem
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
    InvoiceItem,
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
        required=False,
        label="DPH (%)",
        min_value=0,
        initial=21
    )

    def __init__(self, *args, **kwargs):
        # Zachytí argument `user` z view, pokud je poslán
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pokud chceš například filtrovat firemní nabídku podle uživatele:
        if self.user and hasattr(self.user, 'companies'):
            try:
                self.fields['company'].queryset = self.user.companies.all()
            except KeyError:
                # Pokud pole 'company' v modelu není povinné, ignoruj
                pass

    class Meta:
        model = Invoice
        fields = ['issue_date', 'due_date', 'vat_rate', 'is_vat_payer', 'is_paid']

    def clean(self):
        cleaned_data = super().clean()
        is_vat_payer = cleaned_data.get('is_vat_payer', False)

        # Pokud není plátcem DPH → nulová sazba
        if not is_vat_payer:
            cleaned_data['vat_rate'] = None
        elif is_vat_payer and not cleaned_data.get('vat_rate'):
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


# -------------------------------------------------------------------
#                    ACCOUNTING EXPANSION FORMS
# -------------------------------------------------------------------

class AccountingContextForm(forms.ModelForm):
    """Form for selecting/creating accounting context (personal vs organizational)"""

    class Meta:
        model = AccountingContext
        fields = ['name', 'organization', 'accounting_type', 'accounting_method', 'fiscal_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Např. Účetnictví 2025'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'accounting_type': forms.Select(attrs={'class': 'form-control'}),
            'accounting_method': forms.Select(attrs={'class': 'form-control'}),
            'fiscal_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2025'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter organizations to only those the user is a member of
        if self.user:
            from fdk_cz.models import OrganizationMembership
            user_orgs = Organization.objects.filter(
                organizationmembership__user=self.user
            )
            self.fields['organization'].queryset = user_orgs
            self.fields['organization'].required = False

            # Set initial fiscal year to current year
            if not self.instance.pk:
                self.fields['fiscal_year'].initial = timezone.now().year

    def clean(self):
        cleaned_data = super().clean()
        accounting_type = cleaned_data.get('accounting_type')
        organization = cleaned_data.get('organization')

        # If organizational accounting is selected, organization must be provided
        if accounting_type == 'organizational' and not organization:
            self.add_error('organization', 'Pro organizační účetnictví musíte vybrat organizaci.')

        # If personal accounting is selected, organization should be null
        if accounting_type == 'personal' and organization:
            cleaned_data['organization'] = None

        return cleaned_data


class AccountingAccountForm(forms.ModelForm):
    """Form for creating/editing chart of accounts"""

    class Meta:
        model = AccountingAccount
        fields = ['account_number', 'name', 'account_type', 'parent_account', 'description', 'is_active']
        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '221'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bankovní účty'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'parent_account': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        super().__init__(*args, **kwargs)

        # Filter parent accounts to only those in the same context
        if self.context:
            self.fields['parent_account'].queryset = AccountingAccount.objects.filter(
                context=self.context,
                is_active=True
            )


class JournalEntryForm(forms.ModelForm):
    """Form for creating journal entries"""

    class Meta:
        model = JournalEntry
        fields = ['entry_number', 'entry_date', 'description', 'document_number', 'invoice']
        widgets = {
            'entry_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Např. 2025001'}),
            'entry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis účetního případu'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Číslo dokladu'}),
            'invoice': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Set initial entry date to today
        if not self.instance.pk:
            self.fields['entry_date'].initial = timezone.now().date()

        # Filter invoices if needed
        if self.user:
            self.fields['invoice'].queryset = Invoice.objects.filter(
                company__users=self.user
            )
            self.fields['invoice'].required = False


class JournalEntryLineForm(forms.ModelForm):
    """Form for journal entry lines (double-entry bookkeeping)"""

    class Meta:
        model = JournalEntryLine
        fields = ['account', 'debit_amount', 'credit_amount', 'description']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'debit_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'credit_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Popis řádku'}),
        }

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        super().__init__(*args, **kwargs)

        # Filter accounts to only active accounts in the current context
        if self.context:
            self.fields['account'].queryset = AccountingAccount.objects.filter(
                context=self.context,
                is_active=True
            ).order_by('account_number')

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get('debit_amount', 0)
        credit = cleaned_data.get('credit_amount', 0)

        # Only one of debit or credit should have a value
        if debit > 0 and credit > 0:
            raise forms.ValidationError('Položka může být buď MD (debit) nebo D (credit), ne obojí.')

        if debit == 0 and credit == 0:
            raise forms.ValidationError('Musíte vyplnit buď MD (debit) nebo D (credit).')

        return cleaned_data


# Formset for multiple journal entry lines
JournalEntryLineFormSet = modelformset_factory(
    JournalEntryLine,
    form=JournalEntryLineForm,
    extra=2,  # Start with 2 lines (minimum for double-entry)
    can_delete=True,
    min_num=2,  # Require at least 2 lines for double-entry
    validate_min=True
)


class BalanceSheetForm(forms.ModelForm):
    """Form for creating/editing balance sheet entries"""

    class Meta:
        model = BalanceSheet
        fields = ['account', 'balance_type', 'fiscal_year', 'debit_balance', 'credit_balance']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'balance_type': forms.Select(attrs={'class': 'form-control'}),
            'fiscal_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'debit_balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'credit_balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        super().__init__(*args, **kwargs)

        # Filter accounts to current context
        if self.context:
            self.fields['account'].queryset = AccountingAccount.objects.filter(
                context=self.context,
                is_active=True
            ).order_by('account_number')

            # Set initial fiscal year from context
            if not self.instance.pk and self.context:
                self.fields['fiscal_year'].initial = self.context.fiscal_year