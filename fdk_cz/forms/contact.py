# FORMS.CONTACT.PY

from django import forms
from fdk_cz.models import contact, project


"""
class contact_form(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'company', 'description', 'is_private']
"""

class contact_form(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'company', 'description', 'is_private', 'project']

    def __init__(self, *args, **kwargs):
        super(contact_form, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['project'].widget.attrs.update({'class': 'form-control'})
        self.fields['project'].queryset = project.objects.all() 
