# -------------------------------------------------------------------
#                    FORMS.B2B.PY
# -------------------------------------------------------------------
from django import forms
from fdk_cz.models import B2BCompany, B2BContract, B2BDocument, Organization, Project


class B2BCompanyForm(forms.ModelForm):
    """Formulář pro B2B firmu"""

    class Meta:
        model = B2BCompany
        fields = [
            'name', 'legal_name', 'company_id_number', 'tax_id',
            'email', 'phone', 'website',
            'street', 'city', 'postal_code', 'country',
            'category', 'tags', 'organization', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název firmy'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Právní název'}),
            'company_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IČO'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DIČ'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+420 ...'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ulice a číslo popisné'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Město'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PSČ'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'klíčové slovo 1, klíčové slovo 2'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()


class B2BContractForm(forms.ModelForm):
    """Formulář pro B2B smlouvu"""

    class Meta:
        model = B2BContract
        fields = [
            'company', 'organization', 'project',
            'contract_number', 'title', 'description',
            'contract_value', 'currency',
            'start_date', 'end_date', 'signed_date',
            'status', 'categories', 'keywords'
        ]

        tw_input_class = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'

        widgets = {
            'company': forms.Select(attrs={'class': tw_input_class}),
            'organization': forms.Select(attrs={'class': tw_input_class}),
            'project': forms.Select(attrs={'class': tw_input_class}),
            'contract_number': forms.TextInput(attrs={'class': tw_input_class, 'placeholder': 'Číslo smlouvy'}),
            'title': forms.TextInput(attrs={'class': tw_input_class, 'placeholder': 'Název smlouvy'}),
            'description': forms.Textarea(attrs={'class': tw_input_class, 'rows': 4}),
            'contract_value': forms.NumberInput(attrs={'class': tw_input_class, 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': tw_input_class}),
            'start_date': forms.DateInput(attrs={'class': tw_input_class, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': tw_input_class, 'type': 'date'}),
            'signed_date': forms.DateInput(attrs={'class': tw_input_class, 'type': 'date'}),
            'status': forms.Select(attrs={'class': tw_input_class}),
            'categories': forms.TextInput(attrs={'class': tw_input_class, 'placeholder': 'kategorie 1, kategorie 2'}),
            'keywords': forms.TextInput(attrs={'class': tw_input_class, 'placeholder': 'klíčové slovo 1, klíčové slovo 2'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter related objects to only those the user has access to
        if user:
            from django.db.models import Q

            # Filter organizations
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()

            # Filter projects
            self.fields['project'].queryset = Project.objects.filter(
                Q(owner=user) | Q(project_users__user=user)
            ).distinct()


class B2BDocumentForm(forms.ModelForm):
    """Formulář pro B2B dokument"""

    class Meta:
        model = B2BDocument
        fields = [
            'company', 'contract', 'organization',
            'title', 'description',
            'file_path', 'file_url',
            'document_type', 'categories', 'keywords',
            'version'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název dokumentu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file_path': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '/path/to/document.pdf'}),
            'file_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'document_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'smlouva, faktura, nabídka...'}),
            'categories': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kategorie 1, kategorie 2'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'klíčové slovo 1, klíčové slovo 2'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.0'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter related objects to only those the user has access to
        if user:
            from django.db.models import Q

            # Filter organizations
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()
