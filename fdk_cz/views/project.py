# -------------------------------------------------------------------
#                    VIEWS.PROJECT.PY
# -------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Count, Q

from django.utils import timezone


from fdk_cz.forms.project import add_user_form, document_form, category_form, initialize_project_forms, milestone_form, project_form, task_form

import json

from fdk_cz.models import (
    Company,
    Department,
    Employee,
    Organization,
    OrganizationMembership,
    ProjectCategory,
    ProjectComment,
    ProjectDocument,
    ProjectMilestone,
    Project,
    ProjectUser,
    ProjectRole,
    ProjectTask,
    SwotAnalysis,
    TestError
)

from django.shortcuts import render, redirect, get_object_or_404

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------


@login_required
def new_project(request):
    from datetime import date

    # Kontrola limitů projektů před zobrazením formuláře
    # Spočítáme aktivní projekty (bez end_date nebo s end_date >= dnes)
    active_projects_count = Project.objects.filter(
        Q(owner=request.user) | Q(project_users__user=request.user)
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=date.today())
    ).distinct().count()

    # Získáme nebo vytvoříme profil uživatele
    try:
        from fdk_cz.models import UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        max_projects = user_profile.get_max_active_projects()
        is_vip = user_profile.is_vip
    except Exception as e:
        # Fallback pokud tabulka UserProfile neexistuje
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"UserProfile table doesn't exist yet: {e}")
        max_projects = 1  # Výchozí limit pro uživatele bez profilu
        is_vip = False

    # Kontrola limitu - pokud má dosažen limit, nepustit ho dál
    if active_projects_count >= max_projects:
        messages.error(
            request,
            f'Dosáhli jste maximálního počtu aktivních projektů ({max_projects}). '
            f'Pro vytvoření nového projektu ukončete některý ze stávajících projektů nastavením data konce.'
        )
        return redirect('index_project_cs')

    if request.method == 'POST':
        form = project_form(request.POST, user=request.user)
        if form.is_valid():
            # Kontrola limitu znovu před uložením (pro jistotu)
            active_projects_count = Project.objects.filter(
                Q(owner=request.user) | Q(project_users__user=request.user)
            ).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=date.today())
            ).distinct().count()

            if active_projects_count >= max_projects:
                messages.error(
                    request,
                    f'Dosáhli jste maximálního počtu aktivních projektů ({max_projects}).'
                )
                return redirect('index_project_cs')

            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()

            # Přiřadíme uživatele jako administrátora do tabulky project_user
            admin_role = ProjectRole.objects.get(role_name='Administrator')
            ProjectUser.objects.create(
                project=new_project,
                user=request.user,
                role=admin_role
            )

            # Přiřadíme základní kategorie (Frontend, Backend, etc.)
            basic_categories = ['Frontend', 'Backend', 'Database']
            for category_name in basic_categories:
                ProjectCategory.objects.create(
                    name=category_name,
                    project=new_project,  # Specifické pro tento projekt
                    description=f'Základní kategorie: {category_name}'
                )

            messages.success(request, f'Projekt "{new_project.name}" byl úspěšně vytvořen.')
            return redirect('index_project_cs')
    else:
        form = project_form(user=request.user)

    # Přidáme info o limitech do kontextu
    context = {
        'form': form,
        'active_projects_count': active_projects_count,
        'max_projects': max_projects,
        'is_vip': is_vip,
    }
    return render(request, 'project/new_project.html', context)






@login_required
def detail_project(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    all_errors = TestError.objects.filter(project=proj).exclude(status='closed').exclude(deleted=True)    
    members = ProjectUser.objects.filter(project=proj)
    milestones = proj.milestones.all()
    documents = proj.documents.all()
    all_lists = proj.lists.all()

    # Zavolání funkce, která inicializuje formuláře
    form, milestone_form_instance = initialize_project_forms(request.POST if request.method == 'POST' else None)


    # Statistika úkolů dle statusu pro konkrétní projekt
    task_status_counts = proj.tasks.values('status').annotate(count=Count('status'))
    project_status_counts = {
        'Nezahájeno': 0,
        'Probíhá': 0,
        'Hotovo': 0,
    }
    # Přiřazení počtů k jednotlivým statusům
    for item in task_status_counts:
        status = item['status']
        if status in project_status_counts:
            project_status_counts[status] = item['count']
    # Celkový počet úkolů v projektu
    project_total_tasks = sum(project_status_counts.values())


    # Zpracování POST požadavků na přidání uživatele nebo milníku
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data['user']
        role_instance = form.cleaned_data['role']
        project_user_instance, created = ProjectUser.objects.get_or_create(user=user, project=proj)
        project_user_instance.role = role_instance
        project_user_instance.save()
        return redirect('detail_project', project_id=project_id)

    if request.method == 'POST' and 'milestone_form' in request.POST and milestone_form_instance.is_valid():
        new_milestone = milestone_form_instance.save(commit=False)
        new_milestone.project = proj
        new_milestone.save()
        return redirect('detail_project', project_id=project_id)

    tasks_to_do = proj.tasks.exclude(deleted=True).exclude(priority='Nice to have').exclude(status='Hotovo')
    # Další logika pro detaily projektu
    tasks_by_status = {
        'Nezahájeno': proj.tasks.filter(status='Nezahájeno').exclude(deleted=True),
        'Probíhá': proj.tasks.filter(status='Probíhá').exclude(deleted=True),
        'Hotovo': proj.tasks.filter(status='Hotovo').exclude(deleted=True)
    }
    nice_to_have_tasks = proj.tasks.filter(priority='Nice to have').exclude(deleted=True)
    can_view_contacts = request.user.has_perm('project.view_contact') or request.user == proj.owner

    # Kontrola, zda je projekt ukončen (má nastavený end_date a je v minulosti)
    from datetime import date
    is_project_closed = proj.end_date and proj.end_date < date.today()

    # Data pro Ganttův diagram
    gantt_items = []

    # Přidání milníků do Gantt diagramu
    for milestone in milestones:
        if milestone.due_date:
            gantt_items.append({
                'type': 'milestone',
                'title': milestone.title,
                'date': milestone.due_date,
                'status': milestone.status,
            })

    # Přidání vysokoprioritních úkolů do Gantt diagramu
    high_priority_tasks = proj.tasks.filter(priority='Vysoká').exclude(status='Hotovo').exclude(deleted=True)
    for task in high_priority_tasks:
        if task.due_date:  # Fix: Use 'due_date' instead of 'deadline'
            gantt_items.append({
                'type': 'task',
                'title': task.title,
                'date': task.due_date,  # Fix: Use 'due_date' instead of 'deadline'
                'status': task.status,
            })

    # Seřadit podle data
    gantt_items.sort(key=lambda x: x['date'])

    # Přenesení inicializovaných formulářů do šablony
    return render(request, 'project/detail_project.html', {
        'project': proj,
        'all_errors': all_errors,
        'milestones': milestones,
        'milestone_form': milestone_form_instance,
        'documents': documents,
        'all_lists': all_lists,
        'tasks_by_status': tasks_by_status,
        'tasks_to_do': tasks_to_do,
        'nice_to_have_tasks': nice_to_have_tasks,
        'can_view_contacts': can_view_contacts,
        'members': members,
        'form': form,
        'project_status_counts': project_status_counts,
        'project_total_tasks': project_total_tasks,
        'is_project_closed': is_project_closed,
        'gantt_items': gantt_items,
    })







# View for deleting a project
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('index_project')
    return render(request, 'project/delete_project.html', {'project': project})



# View for editing an existing project
@login_required
def edit_project(request, project_id):
    from datetime import date

    # Načtěte projekt, který se má upravit
    project_instance = get_object_or_404(Project, pk=project_id)

    # Kontrola, zda je projekt ukončen (archivován)
    is_project_closed = project_instance.end_date and project_instance.end_date < date.today()
    if is_project_closed:
        messages.error(
            request,
            f'Projekt "{project_instance.name}" je ukončen a nelze jej upravovat. '
            f'Archivované projekty jsou pouze pro čtení.'
        )
        return redirect('detail_project', project_id=project_instance.project_id)

    if request.method == 'POST':
        form = project_form(request.POST, instance=project_instance, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Projekt "{project_instance.name}" byl úspěšně upraven.')
            return redirect('detail_project', project_id=project_instance.project_id)  # Přesměrování na detail projektu po úpravě
    else:
        form = project_form(instance=project_instance, user=request.user)

    return render(request, 'project/edit_project.html', {'form': form, 'project': project_instance})





@login_required
def index_project(request):
    from datetime import date
    from django.core.paginator import Paginator

    # Načteme instanci uživatele podle jeho primárního klíče (ID)
    current_user = User.objects.get(pk=request.user.pk)

    # Base query: user's projects (member or owner)
    base_query = Q(project_users__user=request.user) | Q(owner=request.user)

    # Filter by organization context
    current_org_id = request.session.get('current_organization_id')
    if current_org_id:
        # Organization context: show only projects from this organization
        projects_base = Project.objects.filter(base_query).filter(organization=current_org_id)
    else:
        # Personal context - show ALL user's projects regardless of organization
        projects_base = Project.objects.filter(base_query)

    # Aktivní projekty = bez end_date NEBO s end_date >= dnes
    user_projects = projects_base.filter(
        Q(end_date__isnull=True) | Q(end_date__gte=date.today())
    ).distinct().order_by('-created')

    # Archivované projekty = s end_date < dnes
    archived_projects_query = projects_base.filter(
        end_date__lt=date.today()
    ).distinct().order_by('-end_date')

    # Pagination for archived projects
    archived_page_number = request.GET.get('archived_page', 1)
    archived_paginator = Paginator(archived_projects_query, 12)  # 12 projects per page
    archived_projects = archived_paginator.get_page(archived_page_number)

    assigned_tasks = ProjectTask.objects.filter(assigned=request.user).exclude(deleted=True).order_by('-created')

    # Debug info (odstranit později)
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"User: {request.user.username}")
    logger.info(f"Organization context: {current_org_id}")
    logger.info(f"Active projects count: {user_projects.count()}")
    logger.info(f"Archived projects count: {archived_projects_query.count()}")

    return render(request, 'project/index_project.html', {
        'user_projects': user_projects,
        'archived_projects': archived_projects,
        'assigned_tasks': assigned_tasks
    })







@login_required
def manage_project_users(request, project_id):
    project_instance = get_object_or_404(Project, pk=project_id)
    members = project_instance.project_users.all()

    if request.method == 'POST':
        form = add_user_form(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            send_invitation = form.cleaned_data.get('send_invitation', True)

            try:
                # Pokus o nalezení uživatele podle emailu
                user = User.objects.get(email=email)

                # Kontrola, zda už není v projektu (oprava duplikátní chyby)
                if ProjectUser.objects.filter(project=project_instance, user=user).exists():
                    messages.warning(request, f"Uživatel {user.username} ({email}) je již členem projektu.")
                    return redirect('manage_project_users', project_id=project_id)

                # Přidat uživatele do projektu
                new_member = ProjectUser(
                    project=project_instance,
                    user=user,
                    role=role
                )
                new_member.save()

                # Odeslat notifikaci existujícímu uživateli
                if send_invitation:
                    from fdk_cz.utils.email import send_project_member_added_email
                    send_project_member_added_email(user, project_instance, role, request.user)

                messages.success(request, f"Uživatel {user.username} byl úspěšně přidán do projektu.")
                return redirect('manage_project_users', project_id=project_id)

            except User.DoesNotExist:
                # Uživatel neexistuje - poslat pozvánku
                if send_invitation:
                    from fdk_cz.utils.email import send_project_invitation_email
                    send_project_invitation_email(email, project_instance, role, request.user)
                    messages.info(request, f"Uživatel s emailem {email} není registrován. Byla mu odeslána pozvánka k registraci a přidání do projektu.")
                else:
                    messages.error(request, f"Uživatel s emailem {email} není registrován. Zaškrtněte 'Odeslat pozvánku emailem' pro zaslání registrační pozvánky.")

                return redirect('manage_project_users', project_id=project_id)
    else:
        form = add_user_form()

    return render(request, 'project/manage_project_users.html', {
        'project': project_instance,
        'members': members,
        'form': form,
    })




@login_required
def remove_project_user(request, project_id, user_id):
    project_instance = get_object_or_404(Project, pk=project_id)
    user_instance = get_object_or_404(User, pk=user_id)
    project_user_instance = get_object_or_404(ProjectUser, project=project_instance, user=user_instance)
    project_user_instance.delete()
    return redirect('manage_project_users', project_id=project_id)



# # # T a s k s # # #
"""
@login_required
def create_task(request, project_id):
    proj = get_object_or_404(project, pk=project_id)
    
    if request.method == 'POST':
        form = task_form(request.POST, project=proj)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = proj
            task.creator = request.user.username  # Zde je oprava
            task.save()
            return redirect('detail_project', project_id=project_id)
    else:
        form = task_form(project=proj)
    
    return render(request, 'project/create_task.html', {'form': form, 'project': proj})
"""
@login_required
def create_task(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = task_form(request.POST, project=proj)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = proj
            task.creator = request.user
            task.created = timezone.now()
            task.save()

            # Send email notification if task is assigned
            if task.assigned and task.assigned != request.user:
                from fdk_cz.utils.email import send_task_assignment_email
                send_task_assignment_email(
                    user=task.assigned,
                    task=task,
                    project=proj,
                    assigned_by=request.user
                )

            messages.success(request, f"Úkol '{task.title}' byl vytvořen{' a přiřazen uživateli ' + task.assigned.username if task.assigned else ''}.")
            return redirect('detail_project', project_id=project_id)
    else:
        form = task_form(project=proj)

    return render(request, 'project/create_task.html', {'form': form, 'project': proj})





@login_required
def detail_task(request, task_id):
    task_obj = get_object_or_404(ProjectTask, pk=task_id)
    project = task_obj.project
    comments = task_obj.comments.order_by('-posted')  # Načte komentáře pro úkol

    if request.method == 'POST' and 'comment' in request.POST:
        new_comment = ProjectComment()
        new_comment.task = task_obj
        new_comment.user = request.user
        new_comment.project = task_obj.project  # Zajistí, že nastavujeme instanci projektu
        new_comment.comment = request.POST.get('comment')
        new_comment.posted = timezone.now()
        new_comment.save()
        return redirect('detail_task', task_id=task_id)

    from datetime import date
    return render(request, 'project/detail_task.html', {
        'task': task_obj,
        'project': project,
        'comments': comments,
        'today': date.today()
    })




@login_required
def edit_task(request, task_id):
    task_obj = get_object_or_404(ProjectTask, pk=task_id)
    project = task_obj.project  # Uložení projektu z úkolu
    old_assigned = task_obj.assigned  # Remember who was previously assigned

    if request.method == 'POST':
        form = task_form(request.POST, instance=task_obj, project=project)  # Přidání projektu při POST
        if form.is_valid():
            task = form.save()

            # Send email if task was newly assigned or reassigned to different user
            if task.assigned and task.assigned != old_assigned and task.assigned != request.user:
                from fdk_cz.utils.email import send_task_assignment_email
                send_task_assignment_email(
                    user=task.assigned,
                    task=task,
                    project=project,
                    assigned_by=request.user
                )
                messages.success(request, f"Úkol byl upraven a přiřazen uživateli {task.assigned.username}.")
            else:
                messages.success(request, "Úkol byl úspěšně upraven.")

            # Přesměrování - zpět na projekt nebo task management
            if project:
                return redirect('detail_project', project_id=project.project_id)
            else:
                return redirect('task_management')
    else:
        form = task_form(instance=task_obj, project=project)  # Přidání projektu při GET

    return render(request, 'project/edit_task.html', {'form': form, 'task': task_obj, 'project': project})




@login_required
def delete_task(request, task_id):
    selected_task = get_object_or_404(ProjectTask, pk=task_id)

    if request.method == 'POST':
        # Soft delete
        selected_task.deleted = True
        selected_task.save()
        messages.success(request, "Úkol byl úspěšně smazán.")

        # Přesměrování - zpět na projekt nebo task management
        if selected_task.project:
            return redirect('detail_project', project_id=selected_task.project.project_id)
        else:
            return redirect('task_management')

    return render(request, 'project/delete_task.html', {'selected_task': selected_task})



@login_required
def update_task_status(request, task_id, status):
    selected_task = get_object_or_404(ProjectTask, pk=task_id)  # Načte úkol podle ID
    selected_task.status = status  # Nastaví nový stav
    selected_task.save()  # Uloží změny

    # Přesměrování - zpět na projekt nebo task management
    if selected_task.project:
        return redirect('detail_project', project_id=selected_task.project.project_id)
    else:
        return redirect('task_management')


@login_required
def take_task(request, task_id):
    """Převzetí úkolu uživatelem - nastaví přiřazení a status na Probíhá"""
    selected_task = get_object_or_404(ProjectTask, pk=task_id)
    selected_task.assigned = request.user
    selected_task.status = 'Probíhá'
    selected_task.save()

    # Redirect zpět na detail úkolu
    return redirect('detail_task', task_id=task_id)


@login_required
def task_management(request):
    user = request.user
    # Zobraz úkoly přiřazené uživateli NEBO vytvořené uživatelem
    user_tasks = ProjectTask.objects.filter(
        Q(assigned=user) | Q(creator=user)
    ).exclude(status='Hotovo').exclude(deleted=True).distinct().order_by('priority', '-status')

    # Get organizations where user is member or creator
    user_organizations = Organization.objects.filter(
        Q(created_by=user) | Q(members=user)
    ).distinct()

    # Get projects where user is a member
    user_projects = Project.objects.filter(
        Q(owner=user) | Q(project_users__user=user)
    ).distinct()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        context = request.POST.get('context', 'personal')
        project_id = request.POST.get('project_id')
        organization_id = request.POST.get('organization_id')

        # Validace délky názvu úkolu
        if not title or len(title.strip()) == 0:
            messages.error(request, "Název úkolu je povinný.")
            context_data = {
                'tasks': user_tasks,
                'user_organizations': user_organizations,
                'user_projects': user_projects,
            }
            return render(request, 'project/task_management.html', context_data)

        if len(title) > 255:
            messages.error(request, "Název úkolu je příliš dlouhý. Maximální délka je 255 znaků.")
            context_data = {
                'tasks': user_tasks,
                'user_organizations': user_organizations,
                'user_projects': user_projects,
            }
            return render(request, 'project/task_management.html', context_data)

        # Validace - pokud je vybrán kontext projekt/organizace, musí být vybrán i konkrétní projekt/organizace
        if context == 'project' and not project_id:
            messages.error(request, "Pokud vytváříte projektový úkol, musíte vybrat konkrétní projekt.")
            context_data = {
                'tasks': user_tasks,
                'user_organizations': user_organizations,
                'user_projects': user_projects,
            }
            return render(request, 'project/task_management.html', context_data)

        if context == 'organization' and not organization_id:
            messages.error(request, "Pokud vytváříte organizační úkol, musíte vybrat konkrétní organizaci.")
            context_data = {
                'tasks': user_tasks,
                'user_organizations': user_organizations,
                'user_projects': user_projects,
            }
            return render(request, 'project/task_management.html', context_data)

        task_data = {
            'title': title,
            'description': description,
            'creator': user,
            'priority': 'Nízká',  # Výchozí priorita
            'status': 'Ke zpracování',  # Výchozí status
            'created': timezone.now(),
        }

        # Handle context-specific logic
        if context == 'project' and project_id:
            task_data['project'] = get_object_or_404(Project, pk=project_id)
        elif context == 'organization' and organization_id:
            task_data['organization'] = get_object_or_404(Organization, pk=organization_id)
        # For 'personal' context, no project or organization is set

        ProjectTask.objects.create(**task_data)
        messages.success(request, "Úkol byl úspěšně vytvořen.")
        return redirect('task_management')

    context = {
        'tasks': user_tasks,
        'user_organizations': user_organizations,
        'user_projects': user_projects,
    }
    return render(request, 'project/task_management.html', context)




# # # M i l e s t o n e s # # #@login_required
@login_required
def create_milestone(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = milestone_form(request.POST)
        if form.is_valid():
            new_milestone = form.save(commit=False)
            new_milestone.project = proj
            new_milestone.save()
            return redirect('detail_project', project_id=proj.project_id)
        else:
            # Výpis chyb formuláře pro ladění
            print("Form errors:", form.errors)
    else:
        form = milestone_form()
    
    return render(request, 'project/create_milestone.html', {
        'form': form,
        'project': proj
    })



@login_required
def edit_milestone(request, project_id, milestone_id):
    milestone_instance = get_object_or_404(ProjectMilestone, pk=milestone_id, project_id=project_id)

    if request.method == 'POST':
        form = milestone_form(request.POST, instance=milestone_instance)
        if form.is_valid():
            form.save()
            return redirect('detail_project', project_id=project_id)
    else:
        form = milestone_form(instance=milestone_instance)

    return render(request, 'project/edit_milestone.html', {
        'form': form,
        'project_id': project_id,
        'milestone': milestone_instance
    })



@login_required
def delete_milestone(request, project_id, milestone_id):
    milestone = get_object_or_404(ProjectMilestone, pk=milestone_id, project_id=project_id)

    if request.method == 'POST':
        milestone.delete()
        return redirect('detail_project', project_id=project_id)
    
    return render(request, 'project/delete_milestone.html', {'milestone': milestone, 'project_id': project_id})




### C A T E G O R Y ###
@login_required
def create_category(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = category_form(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.project = proj
            new_category.save()
            return redirect('detail_project', project_id=project_id)
    else:
        form = category_form()
    
    return render(request, 'project/create_category.html', {'form': form, 'project': proj})



@login_required
def edit_category(request, category_id):
    cat = get_object_or_404(ProjectCategory, pk=category_id)
    
    if request.method == 'POST':
        form = category_form(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('detail_project', project_id=cat.project.project_id)
    else:
        form = category_form(instance=cat)
    
    return render(request, 'project/edit_category.html', {'form': form, 'category': cat})



@login_required
def detail_category(request, category_id):
    """Detail kategorie projektu s úkoly a případně informacemi z HR"""
    category = get_object_or_404(ProjectCategory, pk=category_id)
    project = category.project

    # Kontrola přístupu - uživatel musí být členem projektu
    if not ProjectUser.objects.filter(project=project, user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Nemáte přístup k této kategorii.")
        return redirect('index')

    # Získání úkolů v této kategorii
    category_tasks = ProjectTask.objects.filter(category=category, deleted=False).order_by('-created')

    # Rozdělení úkolů podle statusu pro kanban zobrazení
    tasks_by_status = {
        'Nezahájeno': category_tasks.filter(status='Nezahájeno'),
        'Probíhá': category_tasks.filter(status='Probíhá'),
        'Hotovo': category_tasks.filter(status='Hotovo')
    }

    # Statistika úkolů dle statusu
    category_status_counts = {
        'Nezahájeno': tasks_by_status['Nezahájeno'].count(),
        'Probíhá': tasks_by_status['Probíhá'].count(),
        'Hotovo': tasks_by_status['Hotovo'].count(),
    }
    category_total_tasks = sum(category_status_counts.values())

    # Úkoly pro tabulkové zobrazení (nezahájené a probíhající)
    tasks_to_do = category_tasks.exclude(status='Hotovo')

    # Pokud existuje organizace, zkusit najít oddělení se stejným názvem
    department = None
    department_employees = []
    if project.organization:
        try:
            department = Department.objects.get(
                organization=project.organization,
                name__iexact=category.name  # Case-insensitive match
            )
            # Získat zaměstnance z tohoto oddělení
            department_employees = Employee.objects.filter(department=department).select_related('user')
        except Department.DoesNotExist:
            pass

    # Kontrola, zda je projekt ukončen
    is_project_closed = project.end_date is not None

    return render(request, 'project/detail_category.html', {
        'category': category,
        'project': project,
        'tasks_by_status': tasks_by_status,
        'tasks_to_do': tasks_to_do,
        'category_status_counts': category_status_counts,
        'category_total_tasks': category_total_tasks,
        'department': department,
        'department_employees': department_employees,
        'is_project_closed': is_project_closed,
    })


@login_required
def delete_category(request, category_id):
    cat = get_object_or_404(ProjectCategory, pk=category_id)
    project_id = cat.project.project_id
    if request.method == 'POST':
        cat.delete()
        return redirect('detail_project', project_id=project_id)

    return render(request, 'project/delete_category.html', {'category': cat})




#  D O C U M E N T
@login_required
def create_document(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = document_form(request.POST, project_id=project_id)
        if form.is_valid():
            new_document = form.save(commit=False)
            new_document.project = proj
            new_document.save()
            return redirect('detail_project', project_id=project_id)
    else:
        form = document_form(project_id=project_id)

    return render(request, 'project/create_document.html', {'form': form, 'project': proj})





@login_required
def edit_document(request, document_id):
    doc = get_object_or_404(ProjectDocument, pk=document_id)
    if request.method == 'POST':
        form = document_form(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('detail_project', project_id=doc.project.project_id)
    else:
        form = document_form(instance=doc)
    return render(request, 'project/edit_document.html', {'form': form, 'document': doc})

@login_required
def delete_document(request, document_id):
    doc = get_object_or_404(ProjectDocument, pk=document_id)
    project_id = doc.project.project_id
    if request.method == 'POST':
        doc.delete()
        return redirect('detail_project', project_id=project_id)
    return render(request, 'project/delete_document.html', {'document': doc})

@login_required
def detail_document(request, document_id):
    doc = get_object_or_404(ProjectDocument, pk=document_id)
    return render(request, 'project/detail_document.html', {'document': doc})



@login_required
def join_project(request, project_id):
    """
    Allow users to join a project via shareable link
    """
    project_instance = get_object_or_404(Project, pk=project_id)
    user = request.user

    # Check if user is already a member
    if ProjectUser.objects.filter(project=project_instance, user=user).exists():
        messages.info(request, f"Již jste členem projektu '{project_instance.name}'.")
        return redirect('detail_project', project_id=project_id)

    # Get default role (first available) or create "Member" role
    try:
        default_role = ProjectRole.objects.first()
        if not default_role:
            default_role = ProjectRole.objects.create(role_name='Člen')
    except:
        messages.error(request, "Chyba při přidávání do projektu. Kontaktujte administrátora.")
        return redirect('index')

    # Add user to project
    try:
        ProjectUser.objects.create(
            project=project_instance,
            user=user,
            role=default_role
        )
        messages.success(request, f"Byli jste úspěšně přidáni do projektu '{project_instance.name}' s rolí '{default_role.role_name}'.")

        # Send notification to project owner
        if project_instance.owner and project_instance.owner != user:
            from fdk_cz.utils.email import send_email
            send_email(
                recipient=project_instance.owner.email,
                subject=f"Nový člen v projektu {project_instance.name}",
                html_content=f"<p>Uživatel <strong>{user.username}</strong> ({user.email}) se připojil do projektu {project_instance.name} přes sdílený odkaz.</p>",
                text_content=f"Uživatel {user.username} ({user.email}) se připojil do projektu {project_instance.name} přes sdílený odkaz."
            )

        return redirect('detail_project', project_id=project_id)

    except Exception as e:
        messages.error(request, f"Chyba při přidávání do projektu: {str(e)}")
        return redirect('index')


@login_required
def project_log(request, project_id):
    """
    Project activity log - visible only to project administrators
    Shows:
    - Task changes (created, status changes, completed)
    - New documents and edits
    - Errors (including deleted and resolved ones)
    - Comments on tasks
    Paginated by 100 items per page
    """
    from django.core.paginator import Paginator

    project = get_object_or_404(Project, pk=project_id)

    # Check if user is project administrator
    try:
        project_user = ProjectUser.objects.get(project=project, user=request.user)
        if project_user.role.role_name != 'Administrator':
            messages.error(request, "Nemáte oprávnění k zobrazení logu projektu. Pouze administrátoři projektu mají přístup.")
            return redirect('detail_project', project_id=project_id)
    except ProjectUser.DoesNotExist:
        messages.error(request, "Nemáte přístup k tomuto projektu.")
        return redirect('index')

    # Gather all activities
    activities = []

    # 1. Tasks (including deleted and completed)
    tasks = ProjectTask.objects.filter(project=project).order_by('-created')
    for task in tasks:
        # Task creation
        activities.append({
            'type': 'task_deleted' if task.deleted else 'task_created',
            'timestamp': task.created,
            'title': task.title,
            'description': f'Úkol vytvořen uživatelem {task.creator.username if task.creator else "Neznámý"}',
            'status': task.status,
            'user': task.creator,
            'object': task,
            'deleted': task.deleted
        })

        # Task completion (if status is "Hotovo" and task has been updated)
        if task.status == 'Hotovo' and hasattr(task, 'updated') and task.updated:
            activities.append({
                'type': 'task_completed',
                'timestamp': task.updated,
                'title': task.title,
                'description': f'Úkol dokončen',
                'status': task.status,
                'user': task.creator,
                'object': task,
                'deleted': False
            })

    # 2. Documents
    documents = ProjectDocument.objects.filter(project=project).order_by('-uploaded_at')
    for doc in documents:
        activities.append({
            'type': 'document_created',
            'timestamp': doc.uploaded_at,
            'title': doc.title,
            'description': f'Dokument nahrán uživatelem {doc.uploaded_by.username if doc.uploaded_by else "Neznámý"}',
            'user': doc.uploaded_by,
            'object': doc,
            'deleted': False
        })

    # 3. Test Errors (including deleted and resolved)
    errors = TestError.objects.filter(project=project).order_by('-date_created')
    for error in errors:
        # Error creation
        activities.append({
            'type': 'error_deleted' if error.deleted else 'error_created',
            'timestamp': error.date_created,
            'title': error.error_title,
            'description': f'Chyba vytvořena uživatelem {error.created_by.username if error.created_by else "Neznámý"}',
            'status': error.get_status_display(),
            'user': error.created_by,
            'object': error,
            'deleted': error.deleted
        })

        # Error resolution (if status is "Vyřešeno" and has resolution date)
        if error.status == 'resolved' and hasattr(error, 'date_resolved') and error.date_resolved:
            activities.append({
                'type': 'error_resolved',
                'timestamp': error.date_resolved,
                'title': error.error_title,
                'description': f'Chyba vyřešena',
                'status': error.get_status_display(),
                'user': error.created_by,
                'object': error,
                'deleted': False
            })

    # 4. Comments on tasks
    comments = ProjectComment.objects.filter(project=project).order_by('-posted')
    for comment in comments:
        activities.append({
            'type': 'comment_created',
            'timestamp': comment.posted,
            'title': f'Komentář k úkolu: {comment.task.title if comment.task else "Neznámý úkol"}',
            'description': comment.comment[:100] + '...' if len(comment.comment) > 100 else comment.comment,
            'user': comment.user,
            'object': comment,
            'deleted': False
        })

    # Sort all activities by timestamp (newest first)
    activities.sort(key=lambda x: x['timestamp'] if x['timestamp'] else timezone.now(), reverse=True)

    # Paginate activities (100 per page)
    paginator = Paginator(activities, 100)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'project/project_log.html', {
        'project': project,
        'activities': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1
    })


@login_required
def all_project_logs(request):
    """
    View all project activity logs - shows projects where user is administrator
    with activity summaries and links to detailed logs.
    """
    # Get all projects where user is an administrator
    admin_project_users = ProjectUser.objects.filter(
        user=request.user,
        role__role_name='Administrator'
    ).select_related('project', 'project__organization')

    projects_with_stats = []

    for pu in admin_project_users:
        project = pu.project

        # Calculate statistics for each project
        task_count = ProjectTask.objects.filter(project=project).count()
        completed_task_count = ProjectTask.objects.filter(project=project, status='Hotovo').count()
        doc_count = ProjectDocument.objects.filter(project=project).count()
        error_count = TestError.objects.filter(project=project, deleted=False).count()
        open_error_count = TestError.objects.filter(project=project, deleted=False, status='open').count()
        comment_count = ProjectComment.objects.filter(project=project).count()

        # Get last activity date
        last_activity = None

        # Check tasks
        last_task = ProjectTask.objects.filter(project=project).order_by('-created').first()
        if last_task and last_task.created:
            last_activity = last_task.created

        # Check documents
        last_doc = ProjectDocument.objects.filter(project=project).order_by('-uploaded_at').first()
        if last_doc and last_doc.uploaded_at:
            if not last_activity or last_doc.uploaded_at > last_activity:
                last_activity = last_doc.uploaded_at

        # Check errors
        last_error = TestError.objects.filter(project=project).order_by('-date_created').first()
        if last_error and last_error.date_created:
            if not last_activity or last_error.date_created > last_activity:
                last_activity = last_error.date_created

        projects_with_stats.append({
            'project': project,
            'task_count': task_count,
            'completed_task_count': completed_task_count,
            'doc_count': doc_count,
            'error_count': error_count,
            'open_error_count': open_error_count,
            'comment_count': comment_count,
            'last_activity': last_activity,
            'total_activities': task_count + doc_count + error_count + comment_count
        })

    # Sort by last activity (most recent first)
    projects_with_stats.sort(
        key=lambda x: x['last_activity'] if x['last_activity'] else timezone.now() - timezone.timedelta(days=365*10),
        reverse=True
    )

    return render(request, 'project/all_project_logs.html', {
        'projects_with_stats': projects_with_stats,
        'total_projects': len(projects_with_stats)
    })


# -------------------------------------------------------------------
#                    SWOT ANALYSIS
# -------------------------------------------------------------------

@login_required
def list_swot_analyses(request):
    """List all SWOT analyses accessible to user."""
    # Get user's organizations
    user_org_ids = OrganizationMembership.objects.filter(
        user=request.user
    ).values_list('organization_id', flat=True)

    # Get user's projects
    user_project_ids = ProjectUser.objects.filter(
        user=request.user
    ).values_list('project_id', flat=True)

    # Get all accessible SWOT analyses
    swot_analyses = SwotAnalysis.objects.filter(
        Q(organization_id__in=user_org_ids) |
        Q(project_id__in=user_project_ids) |
        Q(owner=request.user)
    ).select_related('organization', 'project', 'created_by').order_by('-updated_at')

    # Filter by context if specified
    context_filter = request.GET.get('context', '')
    if context_filter == 'organization':
        swot_analyses = swot_analyses.filter(organization__isnull=False)
    elif context_filter == 'project':
        swot_analyses = swot_analyses.filter(project__isnull=False)
    elif context_filter == 'personal':
        swot_analyses = swot_analyses.filter(owner=request.user)

    return render(request, 'project/swot_list.html', {
        'swot_analyses': swot_analyses,
        'context_filter': context_filter,
    })


@login_required
def create_swot_analysis(request):
    """Create a new SWOT analysis."""
    # Get user's organizations and projects for the form
    user_organizations = Organization.objects.filter(
        organization_id__in=OrganizationMembership.objects.filter(
            user=request.user
        ).values_list('organization_id', flat=True)
    )
    user_projects = Project.objects.filter(
        project_id__in=ProjectUser.objects.filter(
            user=request.user
        ).values_list('project_id', flat=True)
    )

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        context_type = request.POST.get('context_type', 'personal')

        if not title:
            messages.error(request, 'Název SWOT analýzy je povinný.')
            return render(request, 'project/swot_create.html', {
                'organizations': user_organizations,
                'projects': user_projects,
            })

        # Create SWOT analysis
        swot = SwotAnalysis(
            title=title,
            description=description,
            created_by=request.user,
            strengths=[],
            weaknesses=[],
            opportunities=[],
            threats=[]
        )

        # Set context based on selection
        if context_type == 'organization':
            org_id = request.POST.get('organization_id')
            if org_id:
                swot.organization_id = int(org_id)
        elif context_type == 'project':
            project_id = request.POST.get('project_id')
            if project_id:
                swot.project_id = int(project_id)
        else:  # personal
            swot.owner = request.user

        swot.save()
        messages.success(request, f'SWOT analýza "{title}" byla vytvořena.')
        return redirect('edit_swot_analysis', swot_id=swot.swot_id)

    return render(request, 'project/swot_create.html', {
        'organizations': user_organizations,
        'projects': user_projects,
    })


@login_required
def detail_swot_analysis(request, swot_id):
    """View SWOT analysis detail with visual display."""
    swot = get_object_or_404(SwotAnalysis, swot_id=swot_id)

    # Check access permission
    if not _has_swot_access(request.user, swot):
        messages.error(request, 'Nemáte přístup k této SWOT analýze.')
        return redirect('list_swot_analyses')

    # Sort items by weight (highest first) with original indices
    def sort_with_index(items):
        indexed = [{'text': item.get('text', ''), 'weight': item.get('weight', 5), 'idx': i} for i, item in enumerate(items)]
        return sorted(indexed, key=lambda x: x['weight'], reverse=True)

    return render(request, 'project/swot_detail.html', {
        'swot': swot,
        'sorted_strengths': sort_with_index(swot.strengths),
        'sorted_weaknesses': sort_with_index(swot.weaknesses),
        'sorted_opportunities': sort_with_index(swot.opportunities),
        'sorted_threats': sort_with_index(swot.threats),
    })


@login_required
def edit_swot_analysis(request, swot_id):
    """Edit SWOT analysis - add/update/remove items."""
    swot = get_object_or_404(SwotAnalysis, swot_id=swot_id)

    # Check access permission
    if not _has_swot_access(request.user, swot):
        messages.error(request, 'Nemáte přístup k této SWOT analýze.')
        return redirect('list_swot_analyses')

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'update_metadata':
            swot.title = request.POST.get('title', swot.title).strip()
            swot.description = request.POST.get('description', '').strip()
            swot.save()
            messages.success(request, 'Metadata SWOT analýzy byla aktualizována.')

        elif action == 'add_item':
            quadrant = request.POST.get('quadrant', '')
            text = request.POST.get('text', '').strip()
            weight = int(request.POST.get('weight', 5))

            if text and quadrant in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                items = getattr(swot, quadrant)
                items.append({'text': text, 'weight': min(max(weight, 1), 10)})
                setattr(swot, quadrant, items)
                swot.save()
                messages.success(request, 'Položka byla přidána.')

        elif action == 'update_item':
            quadrant = request.POST.get('quadrant', '')
            index = int(request.POST.get('index', -1))
            text = request.POST.get('text', '').strip()
            weight = int(request.POST.get('weight', 5))

            if quadrant in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                items = getattr(swot, quadrant)
                if 0 <= index < len(items):
                    items[index] = {'text': text, 'weight': min(max(weight, 1), 10)}
                    setattr(swot, quadrant, items)
                    swot.save()
                    messages.success(request, 'Položka byla aktualizována.')

        elif action == 'delete_item':
            quadrant = request.POST.get('quadrant', '')
            index = int(request.POST.get('index', -1))

            if quadrant in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                items = getattr(swot, quadrant)
                if 0 <= index < len(items):
                    del items[index]
                    setattr(swot, quadrant, items)
                    swot.save()
                    messages.success(request, 'Položka byla smazána.')

        elif action == 'save_all':
            # Save all items from JSON
            try:
                swot.strengths = json.loads(request.POST.get('strengths', '[]'))
                swot.weaknesses = json.loads(request.POST.get('weaknesses', '[]'))
                swot.opportunities = json.loads(request.POST.get('opportunities', '[]'))
                swot.threats = json.loads(request.POST.get('threats', '[]'))
                swot.save()
                messages.success(request, 'SWOT analýza byla uložena.')
            except json.JSONDecodeError:
                messages.error(request, 'Chyba při ukládání dat.')

        return redirect('edit_swot_analysis', swot_id=swot.swot_id)

    # Sort items by weight (highest first) with original indices for delete
    def sort_with_index(items):
        indexed = [{'text': item.get('text', ''), 'weight': item.get('weight', 5), 'idx': i} for i, item in enumerate(items)]
        return sorted(indexed, key=lambda x: x['weight'], reverse=True)

    return render(request, 'project/swot_edit.html', {
        'swot': swot,
        'sorted_strengths': sort_with_index(swot.strengths),
        'sorted_weaknesses': sort_with_index(swot.weaknesses),
        'sorted_opportunities': sort_with_index(swot.opportunities),
        'sorted_threats': sort_with_index(swot.threats),
    })


@login_required
def delete_swot_analysis(request, swot_id):
    """Delete SWOT analysis."""
    swot = get_object_or_404(SwotAnalysis, swot_id=swot_id)

    # Check access permission
    if not _has_swot_access(request.user, swot):
        messages.error(request, 'Nemáte přístup k této SWOT analýze.')
        return redirect('list_swot_analyses')

    if request.method == 'POST':
        title = swot.title
        swot.delete()
        messages.success(request, f'SWOT analýza "{title}" byla smazána.')
        return redirect('list_swot_analyses')

    return render(request, 'project/swot_delete.html', {
        'swot': swot,
    })


def _has_swot_access(user, swot):
    """Check if user has access to the SWOT analysis."""
    # Personal SWOT
    if swot.owner and swot.owner == user:
        return True

    # Organization SWOT
    if swot.organization:
        return OrganizationMembership.objects.filter(
            user=user,
            organization=swot.organization
        ).exists()

    # Project SWOT
    if swot.project:
        return ProjectUser.objects.filter(
            user=user,
            project=swot.project
        ).exists()

    return False


# -------------------------------------------------------------------
#                    GANTT DIAGRAM
# -------------------------------------------------------------------

@login_required
def gantt_chart(request):
    """Display Gantt chart for user's projects and tasks."""
    from datetime import date

    # Get projects user has access to
    user_project_ids = ProjectUser.objects.filter(
        user=request.user
    ).values_list('project_id', flat=True)

    # Filter out closed projects (end_date < today)
    projects = Project.objects.filter(
        project_id__in=user_project_ids
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=date.today())  # Only active projects
    ).prefetch_related('tasks', 'milestones').order_by('name')

    # Filter by project if specified
    project_filter = request.GET.get('project', '')
    if project_filter:
        try:
            projects = projects.filter(project_id=int(project_filter))
        except (ValueError, TypeError):
            pass

    # Prepare Gantt data
    gantt_data = []
    for project in projects:
        project_tasks = []
        # Fix: Use correct field names - 'created' and 'title' instead of 'start_date' and 'task_name'
        # Only show high and medium priority tasks
        tasks = project.tasks.filter(
            deleted=False,
            priority__in=['high', 'medium']
        ).order_by('created', 'title')

        for task in tasks:
            # Use 'created' as start date and 'due_date' as end date
            if task.created:
                start_date = task.created.date() if task.created else None
                project_tasks.append({
                    'id': task.task_id,
                    'name': task.title,  # Fix: Use 'title' not 'task_name'
                    'start': start_date.isoformat() if start_date else None,
                    'end': task.due_date.isoformat() if task.due_date else (start_date.isoformat() if start_date else None),
                    'status': task.status,
                    'priority': task.priority,
                    'assignee': task.assigned.get_full_name() if task.assigned else None,  # Fix: Use 'assigned' not 'assignee'
                })

        milestones = []
        for milestone in project.milestones.all():
            if milestone.due_date:
                milestones.append({
                    'id': milestone.milestone_id,
                    'name': milestone.title,  # Fix: Use 'title' not 'milestone_name'
                    'date': milestone.due_date.isoformat(),
                    'completed': milestone.status == 'completed',  # Fix: Check status instead of 'completed' field
                })

        if project_tasks or milestones:
            gantt_data.append({
                'project_id': project.project_id,
                'project_name': project.name,
                'tasks': project_tasks,
                'milestones': milestones,
            })

    # Get all projects for filter dropdown
    all_projects = Project.objects.filter(
        project_id__in=user_project_ids
    ).order_by('name')

    # Convert gantt_data to JSON for JavaScript
    import json as json_module
    for project_data in gantt_data:
        project_data['tasks'] = json_module.dumps(project_data['tasks'])
        project_data['milestones'] = json_module.dumps(project_data['milestones'])

    return render(request, 'project/gantt_chart.html', {
        'gantt_data': gantt_data,
        'all_projects': all_projects,
        'project_filter': project_filter,
    })
