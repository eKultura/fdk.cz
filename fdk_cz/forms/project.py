# FORMS.PROJECT.PY

from django import forms
from django.contrib.auth.models import User
from fdk_cz.models import ProjectCategory, ProjectDocument, ProjectMilestone, Project, ProjectRole, ProjectTask, User


class project_form(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'organization', 'url', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Název projektu', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis projektu', 'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'placeholder': 'URL projektu', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtrovat organizace pouze na ty, kde je uživatel členem nebo vlastníkem
        if user:
            from django.db.models import Q
            from fdk_cz.models import Organization
            self.fields['organization'].queryset = Organization.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()
            self.fields['organization'].required = False
            self.fields['organization'].empty_label = "Bez organizace (osobní projekt)"



class add_user_form(forms.Form):
    email = forms.EmailField(
        label='Email uživatele',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'uzivatel@example.com'
        }),
        help_text='Zadejte email uživatele. Pokud není registrován, bude mu zaslána pozvánka.'
    )
    role = forms.ModelChoiceField(
        queryset=ProjectRole.objects.all(),
        label='Role',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    send_invitation = forms.BooleanField(
        label='Odeslat pozvánku emailem',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Zaškrtněte pro odeslání emailu s pozvánkou do projektu'
    )



class milestone_form(forms.ModelForm):
    class Meta:
        model = ProjectMilestone
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Název milníku'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis milníku'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

def initialize_project_forms(post_data=None):
    """
    Vrací inicializované instance add_user_form a milestone_form,
    připravené pro renderování nebo zpracování POST požadavků.
    """
    user_form = add_user_form(post_data)
    milestone_form_instance = milestone_form(post_data)
    return user_form, milestone_form_instance
    

class task_form(forms.ModelForm):
    # Pole pro výběr nadřazeného úkolu (pro vytvoření podúkolu)
    parent_task = forms.ModelChoiceField(
        queryset=ProjectTask.objects.none(),
        required=False,
        empty_label="--- Hlavní úkol (bez nadřazeného) ---",
        label="Podúkol k úkolu",
        help_text="Pokud chcete vytvořit podúkol, vyberte nadřazený úkol"
    )

    class Meta:
        model = ProjectTask
        fields = ['title', 'description', 'category', 'priority', 'status', 'due_date', 'assigned', 'parent']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Název úkolu'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis úkolu'}),
            'priority': forms.Select(attrs={}),
            'status': forms.Select(attrs={}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned': forms.Select(attrs={}),
            'parent': forms.HiddenInput(),  # Skryté pole, nastavuje se z parent_task
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        parent_task_id = kwargs.pop('parent_task_id', None)  # Pro přímé vytvoření podúkolu
        super().__init__(*args, **kwargs)

        # Kategorie podle projektu
        if project:
            self.fields['category'].queryset = ProjectCategory.objects.filter(project=project)
            self.fields['category'].required = True

            # Filtrovat assigned na členy projektu
            from fdk_cz.models import ProjectUser
            project_members = User.objects.filter(user_projects__project=project).distinct()
            self.fields['assigned'].queryset = project_members

            # Filtrovat parent_task na úkoly stejného projektu (POUZE hlavní úkoly, ne podúkoly)
            main_tasks = ProjectTask.objects.filter(
                project=project,
                parent__isnull=True,  # Pouze hlavní úkoly
                deleted=False
            ).order_by('title')
            self.fields['parent_task'].queryset = main_tasks

            # Pokud vytváříme podúkol k specifickému úkolu
            if parent_task_id:
                try:
                    parent_task = ProjectTask.objects.get(task_id=parent_task_id, project=project)
                    self.initial['parent'] = parent_task
                    self.initial['parent_task'] = parent_task
                    # Zakázat změnu parent, protože je to explicitní podúkol
                    self.fields['parent_task'].disabled = True
                except ProjectTask.DoesNotExist:
                    pass
        else:
            self.fields['category'].queryset = ProjectCategory.objects.none()
            self.fields['category'].required = False
            self.fields['assigned'].queryset = User.objects.all()

        self.fields['category'].empty_label = "Vyberte kategorii"
        self.fields['assigned'].required = False
        self.fields['assigned'].empty_label = "Nepřiřazeno"

    def clean(self):
        cleaned_data = super().clean()
        parent_task = cleaned_data.get('parent_task')
        # Pokud uživatel vybral parent_task, nastav ho jako parent
        if parent_task:
            cleaned_data['parent'] = parent_task
        return cleaned_data




class category_form(forms.ModelForm):
    class Meta:
        model = ProjectCategory
        fields = ['name', 'description'] 
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Název kategorie'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis kategorie'}),
        }



class document_form(forms.ModelForm):
    class Meta:
        model = ProjectDocument
        fields = ['title', 'document_type', 'category', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'summernote'}),
        }

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        if project_id:
            self.fields['category'].queryset = ProjectCategory.objects.filter(project_id=project_id)






