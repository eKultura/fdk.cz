# FORMS.PROJECT.PY

from django import forms
from django.contrib.auth.models import User
from fdk_cz.models import category, document, milestone, project, role, task, User


class project_form(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    class Meta:
        model = project
        fields = ['name', 'description', 'url', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název projektu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis projektu'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL projektu'}),
        }



class add_user_form(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        label='Uživatel', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    role = forms.ModelChoiceField(
        queryset=role.objects.all(),
        label='Role',
        required=True,  # Označení pole role jako povinného
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class milestone_form(forms.ModelForm):
    class Meta:
        model = milestone
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název milníku'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis milníku'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
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
        model = task
        fields = ['title', 'description', 'category', 'priority', 'status', 'due_date', 'assigned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název úkolu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis úkolu'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'assigned': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['category'].queryset = category.objects.filter(project=project)
        else:
            self.fields['category'].queryset = category.objects.none()
        self.fields['category'].empty_label = "Vyberte kategorii"




class category_form(forms.ModelForm):
    class Meta:
        model = category
        fields = ['name', 'description'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název kategorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis kategorie'}),
        }



class document_form(forms.ModelForm):
    class Meta:
        model = document
        fields = ['title', 'document_type', 'category', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'summernote'}),
        }

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        if project_id:
            self.fields['category'].queryset = category.objects.filter(project_id=project_id)






