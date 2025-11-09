# -------------------------------------------------------------------
#                    VIEWS.PROJECT.PY
# -------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Count, Q

from django.utils import timezone


from fdk_cz.forms.project import add_user_form, document_form, category_form, initialize_project_forms, milestone_form, project_form, task_form

from fdk_cz.models import (
    ProjectCategory,
    ProjectComment,
    Company,
    ProjectDocument,
    ProjectMilestone,
    Project,
    ProjectUser,
    ProjectRole,
    ProjectTask,
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
    if request.method == 'POST':
        form = project_form(request.POST, user=request.user)
        if form.is_valid():
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
    return render(request, 'project/new_project.html', {'form': form})






@login_required
def detail_project(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    all_errors = TestError.objects.filter(project=proj)    
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

    tasks_to_do = proj.tasks.exclude(priority='Nice to have').exclude(status='Hotovo')
    # Další logika pro detaily projektu
    tasks_by_status = {
        'Nezahájeno': proj.tasks.filter(status='Nezahájeno'),
        'Probíhá': proj.tasks.filter(status='Probíhá'),
        'Hotovo': proj.tasks.filter(status='Hotovo')
    }
    nice_to_have_tasks = proj.tasks.filter(priority='Nice to have')
    can_view_contacts = request.user.has_perm('project.view_contact') or request.user == proj.owner

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
    })







# View for deleting a project
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('index_project')
    return render(request, 'project/delete_project.html', {'project': project})



# View for editing an existing project 
def edit_project(request, project_id):
    # Načtěte projekt, který se má upravit
    project_instance = get_object_or_404(Project, pk=project_id)

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
    # Načteme instanci uživatele podle jeho primárního klíče (ID)
    current_user = User.objects.get(pk=request.user.pk)
    # Vyhledáme projekty, kde je aktuální uživatel vlastníkem
    user_projects = Project.objects.filter(
        project_users__user=request.user
    ).distinct() 
    assigned_tasks = ProjectTask.objects.filter(assigned=request.user).order_by('-created')

    return render(request, 'project/index_project.html', {'user_projects': user_projects, 'assigned_tasks': assigned_tasks})







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

            return redirect('detail_project', project_id=project.project_id)
    else:
        form = task_form(instance=task_obj, project=project)  # Přidání projektu při GET

    return render(request, 'project/edit_task.html', {'form': form, 'task': task_obj, 'project': project})




@login_required
def delete_task(request, task_id):
    # Načtení úkolu
    selected_task = get_object_or_404(ProjectTask, pk=task_id)

    if request.method == 'POST':
        # Proveďte smazání a nastavte zprávu
        selected_task.delete()
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
    return redirect('detail_project', project_id=selected_task.project.project_id)  




@login_required
def task_management(request):
    user = request.user
    user_tasks = ProjectTask.objects.filter(assigned=user).order_by('priority', '-status')

    user_organizations = user.companies.all()
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

        task_data = {
            'title': title,
            'description': description,
            'creator': user,
            'assigned': user,
        }

        # Handle context-specific logic
        if context == 'project' and project_id:
            task_data['project'] = get_object_or_404(Project, pk=project_id)
        elif context == 'organization' and organization_id:
            task_data['organization'] = get_object_or_404(Company, pk=organization_id)
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
