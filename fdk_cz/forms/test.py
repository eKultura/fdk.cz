# FORMS.TEST.PY
 
 
from django import forms
from fdk_cz.models import test, project, project_user, test_error, test_result, test_type



class test_error_form(forms.ModelForm):
    class Meta:
        model = test_error
        fields = ['project', 'test_result', 'error_title', 'description', 'steps_to_replicate', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(test_error_form, self).__init__(*args, **kwargs)

        # Omezení projektů na ty, které jsou dostupné pro uživatele
        if user:
            user_projects = project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects

        # Nastavení pole test_result jako nepovinného
        self.fields['test_result'].required = False
        self.fields['test_result'].queryset = test_result.objects.none()

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['test_result'].queryset = test_result.objects.filter(project_id=project_id)
            except (ValueError, TypeError):
                self.fields['test_result'].queryset = test_result.objects.none()
        elif self.instance.pk:
            self.fields['test_result'].queryset = self.instance.project.test_results










class test_form(forms.ModelForm):
    GRID_CHOICES = [
        ('a1', 'A1'), ('a2', 'A2'), ('a3', 'A3'),
        ('b1', 'B1'), ('b2', 'B2'), ('b3', 'B3'),
        ('c1', 'C1'), ('c2', 'C2'), ('c3', 'C3'),
    ]

    grid_location = forms.ChoiceField(choices=GRID_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = test
        fields = ['project', 'test_type', 'name', 'description', 'grid_location']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(test_form, self).__init__(*args, **kwargs)

        # Omezení projektů pro daného uživatele
        if user:
            user_projects = project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects

        # Zpočátku prázdná roletka pro typy testů
        self.fields['test_type'].queryset = test_type.objects.none()

        if 'project' in self.data:
            try:
                selected_project_id = int(self.data.get('project'))
                self.fields['test_type'].queryset = test_type.objects.filter(project_id=selected_project_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['test_type'].queryset = self.instance.project.test_types

        # Bootstrap stylování pro všechny pole
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})





class test_type_form(forms.ModelForm):
    class Meta:
        model = test_type
        fields = ['project', 'name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Bezpečně odstraníme 'user', pokud není přítomen
        super(test_type_form, self).__init__(*args, **kwargs)

        # Pokud byl předán uživatel, omezíme projekty na ty, ke kterým má uživatel přístup
        if user:
            user_projects = project.objects.filter(project_users__user=user)
            self.fields['project'].queryset = user_projects
        else:
            self.fields['project'].queryset = project.objects.all()  # Pokud není uživatel, načteme všechny projekty

        # Stylování formulářových polí
        self.fields['project'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})









class test_result_form(forms.ModelForm):
    class Meta:
        model = test_result
        fields = ['project', 'test', 'executed_by', 'result']