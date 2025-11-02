# -------------------------------------------------------------------
#                    FORMS.RISK.PY
# -------------------------------------------------------------------
from django import forms
from fdk_cz.models import Risk, Project, Organization


class RiskForm(forms.ModelForm):
    """Formulář pro riziko"""

    class Meta:
        model = Risk
        fields = [
            'title', 'description', 'project', 'organization',
            'category', 'probability', 'impact',
            'mitigation_strategy', 'contingency_plan',
            'status', 'owner'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název rizika'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'probability': forms.Select(attrs={'class': 'form-control'}),
            'impact': forms.Select(attrs={'class': 'form-control'}),
            'mitigation_strategy': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contingency_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields optional
        self.fields['project'].required = False
        self.fields['organization'].required = False
        self.fields['owner'].required = False

        # Filter related objects to only those the user has access to
        if user:
            from django.db.models import Q

            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()

            self.fields['project'].queryset = Project.objects.filter(
                Q(owner=user) | Q(project_users__user=user)
            ).distinct()
