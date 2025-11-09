# FORMS.TEST.PY
 
 
from django import forms
from fdk_cz.models import Test, Project, ProjectUser, TestError, TestResult, TestType



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










class test_form(forms.ModelForm):
    GRID_CHOICES = [
        ('a1', 'A1'), ('a2', 'A2'), ('a3', 'A3'),
        ('b1', 'B1'), ('b2', 'B2'), ('b3', 'B3'),
        ('c1', 'C1'), ('c2', 'C2'), ('c3', 'C3'),
    ]

    grid_location = forms.ChoiceField(choices=GRID_CHOICES, widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}))

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

        # Zpočátku prázdná roletka pro typy testů
        self.fields['test_type'].queryset = TestType.objects.none()

        if 'project' in self.data:
            try:
                selected_project_id = int(self.data.get('project'))
                self.fields['test_type'].queryset = TestType.objects.filter(project_id=selected_project_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['test_type'].queryset = self.instance.project.test_types

        # Tailwind stylování pro všechny pole
        tailwind_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        for field_name, field in self.fields.items():
            if field_name == 'description':
                # Textarea má trochu jiné classes
                field.widget.attrs.update({'class': tailwind_classes, 'rows': '4'})
            else:
                field.widget.attrs.update({'class': tailwind_classes})





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

        # Tailwind stylování formulářových polí
        tailwind_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        self.fields['project'].widget.attrs.update({'class': tailwind_classes})
        self.fields['name'].widget.attrs.update({'class': tailwind_classes})
        self.fields['description'].widget.attrs.update({'class': tailwind_classes, 'rows': '4'})









class test_result_form(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['project', 'test', 'executed_by', 'result']