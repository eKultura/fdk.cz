# -------------------------------------------------------------------
#                    FORMS.ASSET.PY
# -------------------------------------------------------------------
from django import forms
from fdk_cz.models import Asset, AssetCategory, Organization


class AssetForm(forms.ModelForm):
    """Formulář pro majetek"""

    class Meta:
        model = Asset
        fields = [
            'name', 'asset_number', 'description',
            'category', 'organization', 'location', 'responsible_person',
            'purchase_date', 'purchase_price', 'current_value', 'currency',
            'status', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název majetku'}),
            'asset_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Číslo majetku (unikátní)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Umístění'}),
            'responsible_person': forms.Select(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields optional
        self.fields['category'].required = False
        self.fields['responsible_person'].required = False

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()

            # Filter categories based on selected organization
            # Use try/except to handle RelatedObjectDoesNotExist when organization is not set
            try:
                if self.instance and self.instance.pk and self.instance.organization:
                    self.fields['category'].queryset = AssetCategory.objects.filter(
                        organization=self.instance.organization
                    )
                else:
                    self.fields['category'].queryset = AssetCategory.objects.filter(
                        organization__in=self.fields['organization'].queryset
                    )
            except:
                # If organization is not set, filter by user's organizations
                self.fields['category'].queryset = AssetCategory.objects.filter(
                    organization__in=self.fields['organization'].queryset
                )


class AssetCategoryForm(forms.ModelForm):
    """Formulář pro kategorii majetku"""

    class Meta:
        model = AssetCategory
        fields = ['name', 'description', 'organization', 'parent_category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název kategorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'parent_category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make parent_category optional
        self.fields['parent_category'].required = False

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()

            # Filter parent categories based on selected organization
            # Use try/except to handle RelatedObjectDoesNotExist when organization is not set
            try:
                if self.instance and self.instance.pk and self.instance.organization:
                    self.fields['parent_category'].queryset = AssetCategory.objects.filter(
                        organization=self.instance.organization
                    ).exclude(pk=self.instance.pk)
                else:
                    self.fields['parent_category'].queryset = AssetCategory.objects.filter(
                        organization__in=self.fields['organization'].queryset
                    )
            except:
                # If organization is not set, filter by user's organizations
                self.fields['parent_category'].queryset = AssetCategory.objects.filter(
                    organization__in=self.fields['organization'].queryset
                )
