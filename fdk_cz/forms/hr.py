# -------------------------------------------------------------------
#                    FORMS.HR.PY
# -------------------------------------------------------------------
from django import forms
from fdk_cz.models import Employee, Department, Organization, User


class EmployeeForm(forms.ModelForm):
    """Formulář pro zaměstnance"""

    class Meta:
        model = Employee
        fields = [
            'user', 'first_name', 'last_name', 'personal_id_number',
            'email', 'phone',
            'organization', 'department', 'position', 'employee_number',
            'employment_type', 'hire_date', 'termination_date', 'status',
            'salary', 'currency', 'notes'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jméno'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Příjmení'}),
            'personal_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rodné číslo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+420 ...'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pozice'}),
            'employee_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Číslo zaměstnance'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'termination_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make user field optional
        self.fields['user'].required = False

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()

            # Filter departments based on selected organization
            if self.instance and self.instance.organization:
                self.fields['department'].queryset = Department.objects.filter(
                    organization=self.instance.organization
                )
            else:
                self.fields['department'].queryset = Department.objects.filter(
                    organization__in=self.fields['organization'].queryset
                )


class DepartmentForm(forms.ModelForm):
    """Formulář pro oddělení"""

    class Meta:
        model = Department
        fields = ['name', 'description', 'organization', 'parent_department', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název oddělení'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'parent_department': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields optional
        self.fields['parent_department'].required = False
        self.fields['manager'].required = False

        # Filter organizations to only those the user has access to
        if user:
            from django.db.models import Q
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()

            # Filter parent departments based on selected organization
            if self.instance and self.instance.organization:
                self.fields['parent_department'].queryset = Department.objects.filter(
                    organization=self.instance.organization
                ).exclude(pk=self.instance.pk)
