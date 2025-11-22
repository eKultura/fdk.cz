# -------------------------------------------------------------------
#                    VIEWS.CONTACT.PY
# -------------------------------------------------------------------
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from fdk_cz.models import Contact, Project, ProjectUser, ProjectRole, User
from fdk_cz.forms.contact import contact_form

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------


# Vytvoření nového kontaktu
@login_required
def create_contact(request, project_id=None):
    """Vytvoření nového kontaktu, s možností přednastavení projektu"""
    # Získáme projekty, kde má uživatel roli (nemusí být admin)
    user_projects = ProjectUser.objects.filter(user=request.user)
    available_projects = Project.objects.filter(project_id__in=[up.project_id for up in user_projects])

    # Přednostně použijeme project_id z URL, pak z GET parametru
    selected_project_id = project_id or request.GET.get('id_projektu')
    selected_project = available_projects.filter(pk=selected_project_id).first() if selected_project_id else None

    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.account = request.user
            # Pokud byl projekt přednastavený z URL a není v POST datech (disabled field)
            if selected_project and not new_contact.project:
                new_contact.project = selected_project
            new_contact.save()
            # Přesměrovat na detail projektu pokud byl projekt přednastavený
            if selected_project:
                return redirect('detail_project', project_id=selected_project.project_id)
            return redirect('my_contacts')
    else:
        form = contact_form()
        form.fields['project'].queryset = available_projects
        if selected_project:
            form.fields['project'].initial = selected_project.project_id

    return render(request, 'contact/create_contact.html', {
        'form': form,
        'projects': available_projects,
        'preselected_project': selected_project,
    })


@login_required
def edit_contact(request, contact_id):
    contact_instance = get_object_or_404(Contact, pk=contact_id)

    # ✅ OPRAVA: Získání projektů, kde je uživatel vlastníkem nebo administrátorem
    # Použití get_or_create místo get
    admin_role, _ = ProjectRole.objects.get_or_create(role_name='Administrator')
    owner_role, _ = ProjectRole.objects.get_or_create(role_name='Owner')

    user_projects = ProjectUser.objects.filter(user=request.user, role__in=[admin_role, owner_role])

    if request.method == 'POST':
        form = contact_form(request.POST, instance=contact_instance)
        if form.is_valid():
            contact = form.save()
            # Po editaci vždy zpět na seznam kontaktů
            return redirect('my_contacts')
    else:
        form = contact_form(instance=contact_instance)
        form.fields['project'].queryset = Project.objects.filter(
            project_id__in=[user_project.project_id for user_project in user_projects]
        )

    return render(request, 'contact/edit_contact.html', {
        'form': form,
        'projects': user_projects,
        'contact': contact_instance
    })


@login_required
def list_contacts(request):
    # ✅ OPRAVA: Získáme role vlastníka a administrátora
    # Použití get_or_create místo get - vytvoří role, pokud neexistují
    admin_role, _ = ProjectRole.objects.get_or_create(role_name='Administrator')
    owner_role, _ = ProjectRole.objects.get_or_create(role_name='Owner')

    # Získáme projekty, kde je uživatel vlastníkem nebo administrátorem
    user_projects = ProjectUser.objects.filter(user=request.user, role__in=[admin_role, owner_role])

    # Získání projektů, které odpovídají uživateli
    projects = Project.objects.filter(project_id__in=[user_project.project_id for user_project in user_projects])

    # Kontakty filtrované podle projektů
    selected_project_id = request.GET.get('project_id', None)

    if selected_project_id:
        contacts = Contact.objects.filter(project_id=selected_project_id, account=request.user)
    else:
        contacts = Contact.objects.filter(account=request.user)

    # Přidáme stránkování
    paginator = Paginator(contacts, 10)  # 10 kontaktů na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contact/list_contacts.html', {
        'contacts': page_obj,
        'projects': projects, 
        'project_id': selected_project_id
    })


# Detail kontaktu
@login_required
def detail_contact(request, contact_id):
    contact_instance = get_object_or_404(Contact, pk=contact_id)
    
    # Pokud je kontakt soukromý, ověřit oprávnění
    if contact_instance.is_private and contact_instance.account != request.user:
        return redirect('my_contacts')  # Nemá oprávnění
    
    return render(request, 'contact/detail_contact.html', {'contact': contact_instance})


@login_required
def delete_contact(request, contact_id):
    contact_instance = get_object_or_404(Contact, pk=contact_id)
    
    # Ověření, že uživatel má oprávnění ke smazání kontaktu
    if contact_instance.is_private and contact_instance.account != request.user:
        return redirect('my_contacts')  # Nemá oprávnění
    
    if request.method == 'POST':
        contact_instance.delete()
        return redirect('my_contacts')
    
    return render(request, 'contact/delete_contact.html', {'contact': contact_instance})