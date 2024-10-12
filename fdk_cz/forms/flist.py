# FORMS.FLIST.PY


from django import forms
from django.utils import timezone

from fdk_cz.models import flist, list_item, project, project_user



class list_form(forms.ModelForm):
    class Meta:
        model = flist
        fields = ['name', 'description', 'is_private', 'project']

    def __init__(self, *args, **kwargs):
        # Předání uživatele přes kwargs
        user = kwargs.pop('user', None)
        super(list_form, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['project'].widget.attrs.update({'class': 'form-control'})
        self.fields['project'].required = False  # Projekt není povinný

        if user:
            # Získáme projekty přiřazené uživateli
            user_projects = project_user.objects.filter(user=user).values_list('project', flat=True)
            self.fields['project'].queryset = project.objects.filter(pk__in=user_projects)





class list_item_form(forms.ModelForm):
    class Meta:
        model = list_item
        fields = ['content', 'item_order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['item_order'].widget.attrs.update({'class': 'form-control', 'min': '1'})  # Atribut min=1

    def clean_item_order(self):
        item_order = self.cleaned_data.get('item_order')
        if item_order < 1:
            raise forms.ValidationError('Pořadí musí být větší nebo rovno 1.')
        return item_order


