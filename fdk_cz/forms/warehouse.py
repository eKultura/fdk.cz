from django import forms
from fdk_cz.models import Warehouse, WarehouseItem, WarehouseTransaction, WarehouseCategory, Project, Organization

class transaction_form(forms.ModelForm):
    class Meta:
        model = WarehouseTransaction
        fields = ['transaction_type', 'quantity']
        labels = {
            'transaction_type': 'Typ transakce',
            'quantity': 'Množství',
        }
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Zadejte množství'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].empty_label = "Vyberte typ transakce"


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'project', 'organization']
        labels = {
            'name': 'Název skladu',
            'location': 'Umístění',
            'project': 'Projekt',
            'organization': 'Organizace',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např: Hlavní sklad'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např: Praha, Sklad A'
            }),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].empty_label = "--- Vyberte projekt (volitelné) ---"
        self.fields['organization'].empty_label = "--- Vyberte organizaci (volitelné) ---"


class WarehouseItemForm(forms.ModelForm):
    class Meta:
        model = WarehouseItem
        fields = ['name', 'description', 'quantity', 'category']
        labels = {
            'name': 'Název položky',
            'description': 'Popis',
            'quantity': 'Počáteční množství',
            'category': 'Kategorie',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např: Šrouby M6'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Podrobný popis položky...'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "--- Vyberte kategorii (volitelné) ---"


class WarehouseCategoryForm(forms.ModelForm):
    class Meta:
        model = WarehouseCategory
        fields = ['name', 'description']
        labels = {
            'name': 'Název kategorie',
            'description': 'Popis',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např: Spojovací materiál'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Popis kategorie...'
            }),
        }
