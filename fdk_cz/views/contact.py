# VIEWS.CONTACT.PY

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from fdk_cz.models import contact, project, project_user, role, user
from fdk_cz.forms.contact import contact_form


# Vytvoření nového kontaktu
@login_required
def create_contact(request, project_id=None, account_id=None):
    # Získání projektů, kde je uživatel vlastníkem nebo administrátorem
    admin_role = role.objects.get(role_name='Administrator')
    owner_role = role.objects.get(role_name='Owner')
    user_projects = project_user.objects.filter(user=request.user, role__in=[admin_role, owner_role])

    # Pokud je projekt předán přes URL
    selected_project_id = request.GET.get('id_projektu')
    selected_project = None
    if selected_project_id:
        selected_project = project.objects.filter(pk=selected_project_id, project_id__in=[user_project.project_id for user_project in user_projects]).first()

    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.account = request.user
            if selected_project:
                new_contact.project = selected_project
            new_contact.save()
            return redirect('my_contacts')
    else:
        form = contact_form()
        form.fields['project'].queryset = project.objects.filter(project_id__in=[user_project.project_id for user_project in user_projects])
        if selected_project:
            form.fields['project'].initial = selected_project

    return render(request, 'contact/create_contact.html', {'form': form, 'projects': user_projects})



@login_required
def edit_contact(request, contact_id):
    contact_instance = get_object_or_404(contact, pk=contact_id)

    # Získání projektů, kde je uživatel vlastníkem nebo administrátorem
    admin_role = role.objects.get(role_name='Administrator')
    owner_role = role.objects.get(role_name='Owner')
    user_projects = project_user.objects.filter(user=request.user, role__in=[admin_role, owner_role])

    if request.method == 'POST':
        form = contact_form(request.POST, instance=contact_instance)
        if form.is_valid():
            form.save()
            return redirect('my_contacts')
    else:
        form = contact_form(instance=contact_instance)
        form.fields['project'].queryset = project.objects.filter(project_id__in=[user_project.project_id for user_project in user_projects])

    return render(request, 'contact/edit_contact.html', {'form': form, 'projects': user_projects})




@login_required
def list_contacts(request):
    # Získáme role vlastníka a administrátora
    admin_role = role.objects.get(role_name='Administrator')
    owner_role = role.objects.get(role_name='Owner')

    # Získáme projekty, kde je uživatel vlastníkem nebo administrátorem
    user_projects = project_user.objects.filter(user=request.user, role__in=[admin_role, owner_role])

    # Získání projektů, které odpovídají uživateli
    projects = project.objects.filter(project_id__in=[user_project.project_id for user_project in user_projects])

    # Kontakty filtrované podle projektů
    selected_project_id = request.GET.get('project_id', None)

    if selected_project_id:
        contacts = contact.objects.filter(project_id=selected_project_id, account=request.user)
    else:
        contacts = contact.objects.filter(account=request.user)

    # Přidáme stránkování
    paginator = Paginator(contacts, 10)  # 10 kontaktů na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contact/list_contacts.html', {
        'contacts': page_obj,
        'projects': projects, 
        'project_id': selected_project_id
    })




# Editace kontaktu
"""
@login_required
def edit_contact(request, contact_id):
    contact_instance = get_object_or_404(contact, pk=contact_id)
    
    # Ověření, že uživatel má oprávnění k editaci kontaktu
    if contact_instance.is_private and contact_instance.account != request.user:
        return redirect('my_contacts')  # Nemá oprávnění
    
    if request.method == 'POST':
        form = contact_form(request.POST, instance=contact_instance)
        if form.is_valid():
            form.save()
            if contact_instance.project:
                return redirect('detail_project', project_id=contact_instance.project.project_id)
            return redirect('my_contacts')
    else:
        form = contact_form(instance=contact_instance)
    
    return render(request, 'contact/edit_contact.html', {'form': form})
"""


# Detail kontaktu
@login_required
def detail_contact(request, contact_id):
    contact_instance = get_object_or_404(contact, pk=contact_id)
    
    # Pokud je kontakt soukromý, ověřit oprávnění
    if contact_instance.is_private and contact_instance.account != request.user:
        return redirect('my_contacts')  # Nemá oprávnění
    
    return render(request, 'contact/detail_contact.html', {'contact': contact_instance})




@login_required
def delete_contact(request, contact_id):
    contact_instance = get_object_or_404(contact, pk=contact_id)
    
    # Ověření, že uživatel má oprávnění ke smazání kontaktu
    if contact_instance.is_private and contact_instance.account != request.user:
        return redirect('my_contacts')  # Nemá oprávnění
    
    if request.method == 'POST':
        contact_instance.delete()
        return redirect('my_contacts')
    
    return render(request, 'contact/delete_contact.html', {'contact': contact_instance})
