# FORMS.TEST.PY
 
 
from django import forms
from django.db.models import Q
from fdk_cz.models import Test, Project, ProjectUser, TestError, TestResult, TestType, TestScenario, Organization



class test_error_form(forms.ModelForm):
    class Meta:
        model = TestError
        fields = ['project', 'test_result', 'error_title', 'description', 'steps_to_replicate', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(test_error_form, self).__init__(*args, **kwargs)

        # Omezení projektů na ty, které jsou dostupné pro uživatele
        if user:
            user_projects = Project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects

        # Pokud je projekt přednastavený (z initial), zamknout pole
        if self.initial.get('project'):
            self.fields['project'].disabled = True
            self.fields['project'].widget.attrs['readonly'] = True

        # Nastavení pole test_result jako nepovinného
        self.fields['test_result'].required = False
        self.fields['test_result'].queryset = TestResult.objects.none()

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['test_result'].queryset = TestResult.objects.filter(project_id=project_id)
            except (ValueError, TypeError):
                self.fields['test_result'].queryset = TestResult.objects.none()
        elif self.instance.pk:
            self.fields['test_result'].queryset = self.instance.project.test_results
        elif self.initial.get('project'):
            # Načíst test results pro přednastavený projekt
            try:
                project_id = int(self.initial.get('project'))
                self.fields['test_result'].queryset = TestResult.objects.filter(project_id=project_id)
            except (ValueError, TypeError):
                pass










class test_form(forms.ModelForm):
    GRID_CHOICES = [
        ('a1', 'A1'), ('a2', 'A2'), ('a3', 'A3'),
        ('b1', 'B1'), ('b2', 'B2'), ('b3', 'B3'),
        ('c1', 'C1'), ('c2', 'C2'), ('c3', 'C3'),
    ]

    grid_location = forms.ChoiceField(choices=GRID_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Test
        fields = ['project', 'test_type', 'name', 'description', 'grid_location']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(test_form, self).__init__(*args, **kwargs)

        # Omezení projektů pro daného uživatele
        if user:
            user_projects = Project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects

        # Načíst typy testů podle vybraného projektu
        if 'project' in self.data:
            # Pokud je projekt v POST datech (formulář byl odeslán)
            try:
                selected_project_id = int(self.data.get('project'))
                self.fields['test_type'].queryset = TestType.objects.filter(project_id=selected_project_id)
            except (ValueError, TypeError):
                # Pokud projekt není validní, zobrazit všechny typy testů
                self.fields['test_type'].queryset = TestType.objects.all()
        elif self.instance.pk:
            # Pokud editujeme existující test, načíst typy testů pro jeho projekt
            self.fields['test_type'].queryset = self.instance.project.test_types
        elif self.initial.get('project'):
            # Pokud je projekt předán v initial (předvybraný)
            try:
                project_id = int(self.initial.get('project'))
                self.fields['test_type'].queryset = TestType.objects.filter(project_id=project_id)
            except (ValueError, TypeError):
                self.fields['test_type'].queryset = TestType.objects.all()
        else:
            # Pokud není vybrán projekt, zobrazit všechny dostupné typy testů
            # (uživatel musí nejdřív vybrat projekt)
            if user:
                # Zobrazit test types pro projekty uživatele
                user_project_ids = Project.objects.filter(project_users__user=user).values_list('project_id', flat=True)
                self.fields['test_type'].queryset = TestType.objects.filter(project_id__in=user_project_ids)
            else:
                self.fields['test_type'].queryset = TestType.objects.all()

        # Form control styling
        for field_name, field in self.fields.items():
            if field_name == 'description':
                field.widget.attrs.update({'class': 'form-control', 'rows': '4'})
            elif field_name != 'grid_location':  # grid_location má už class nastavený
                field.widget.attrs.update({'class': 'form-control'})





class test_type_form(forms.ModelForm):
    class Meta:
        model = TestType
        fields = ['project', 'name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Bezpečně odstraníme 'user', pokud není přítomen
        super(test_type_form, self).__init__(*args, **kwargs)

        # Pokud byl předán uživatel, omezíme projekty na ty, ke kterým má uživatel přístup
        if user:
            user_projects = Project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects
        else:
            self.fields['project'].queryset = Project.objects.all()  # Pokud není uživatel, načteme všechny projekty

        # Form control styling
        self.fields['project'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': '4'})









class test_result_form(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['project', 'test', 'executed_by', 'result']

class TestScenarioForm(forms.ModelForm):
    """Formulář pro vytváření a editaci testovacích scénářů"""
    
    class Meta:
        model = TestScenario
        fields = ['name', 'description', 'steps', 'expected_result', 
                  'organization', 'project', 'owner', 'priority', 'status']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TestScenarioForm, self).__init__(*args, **kwargs)
        
        # Filtrování organizací a projektů podle uživatele
        if user:
            # Organizace, kde je uživatel členem
            user_orgs = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()
            self.fields['organization'].queryset = user_orgs

            # Projekty uživatele
            user_projects = Project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects

            # Uživatelé pro pole owner - filtrujeme pouze z organizací uživatele
            from django.contrib.auth import get_user_model
            User = get_user_model()
            self.fields['owner'].queryset = User.objects.filter(
                Q(created_organizations__in=user_orgs) |
                Q(organizationmembership__organization__in=user_orgs)
            ).distinct()
            
            # Nastavení výchozího ownera na aktuálního uživatele
            if not self.instance.pk:
                self.fields['owner'].initial = user
        
        # Volitelná pole
        self.fields['organization'].required = False
        self.fields['project'].required = False
        self.fields['owner'].required = False
        self.fields['description'].required = False
        self.fields['expected_result'].required = False
        
        # Styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': '4'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
