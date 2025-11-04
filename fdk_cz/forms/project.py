# FORMS.PROJECT.PY

from django import forms
from django.contrib.auth.models import User
from fdk_cz.models import ProjectCategory, ProjectDocument, ProjectMilestone, Project, ProjectRole, ProjectTask, User


class project_form(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'url', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Název projektu'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis projektu'}),
            'url': forms.TextInput(attrs={'placeholder': 'URL projektu'}),
        }



class add_user_form(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        label='Uživatel', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    role = forms.ModelChoiceField(
        queryset=ProjectRole.objects.all(),
        label='Role',
        required=True,  # Označení pole role jako povinného
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class milestone_form(forms.ModelForm):
    class Meta:
        model = ProjectMilestone
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Název milníku'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis milníku'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={}),
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
    class Meta:
        model = ProjectTask
        fields = ['title', 'description', 'category', 'priority', 'status', 'due_date', 'assigned']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Název úkolu'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Popis úkolu'}),
            'priority': forms.Select(attrs={}),
            'status': forms.Select(attrs={}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned': forms.Select(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['category'].queryset = ProjectCategory.objects.filter(project=project)
        else:
            self.fields['category'].queryset = ProjectCategory.objects.none()
        self.fields['category'].empty_label = "Vyberte kategorii"




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






