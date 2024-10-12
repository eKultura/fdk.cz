# FORMS.PROJECT.PY

from django import forms
from django.contrib.auth.models import User
from fdk_cz.models import category, milestone, project, role, task



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
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Uživatel', widget=forms.Select(attrs={'class': 'form-control'}))
    role = forms.ModelChoiceField(queryset=role.objects.all(), label='Role', widget=forms.Select(attrs={'class': 'form-control'}))

class category_form(forms.ModelForm):
    class Meta:
        model = category
        fields = ['name', 'description'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název kategorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis kategorie'}),
        }

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
            self.fields['category'].queryset = category.objects.filter(project__in=[project, None])

