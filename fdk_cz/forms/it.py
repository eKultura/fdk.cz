# -------------------------------------------------------------------
#                    FORMS.IT.PY
# -------------------------------------------------------------------
from django import forms
from fdk_cz.models import ITAsset, ITIncident, Organization


class ITAssetForm(forms.ModelForm):
    """Formulář pro IT aktivum"""

    class Meta:
        model = ITAsset
        fields = [
            'name', 'asset_tag', 'description',
            'asset_type', 'manufacturer', 'model', 'serial_number',
            'organization', 'assigned_to',
            'purchase_date', 'purchase_price', 'warranty_expiry',
            'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název aktiva'}),
            'asset_tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Tag (unikátní)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Výrobce'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sériové číslo'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'warranty_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields optional
        self.fields['assigned_to'].required = False

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(owner=user) | Q(organization_users__user=user)
            ).distinct()


class ITIncidentForm(forms.ModelForm):
    """Formulář pro IT incident (ITIL)"""

    class Meta:
        model = ITIncident
        fields = [
            'title', 'description', 'incident_number',
            'organization', 'affected_asset',
            'assigned_to', 'priority', 'status',
            'resolution_notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název incidentu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'incident_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INC-001'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'affected_asset': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'resolution_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields optional
        self.fields['affected_asset'].required = False
        self.fields['assigned_to'].required = False
        self.fields['resolution_notes'].required = False

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(owner=user) | Q(organization_users__user=user)
            ).distinct()

            # Filter IT assets
            if self.instance and self.instance.organization:
                self.fields['affected_asset'].queryset = ITAsset.objects.filter(
                    organization=self.instance.organization
                )
            else:
                self.fields['affected_asset'].queryset = ITAsset.objects.filter(
                    organization__in=self.fields['organization'].queryset
                )
