# views.project.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from fdk_cz.forms.project import add_user_form, category_form, milestone_form, project_form, task_form
from fdk_cz.models import category, milestone, project, project_user, role, task

from django.shortcuts import render, redirect, get_object_or_404






@login_required
def new_project(request):
    if request.method == 'POST':
        form = project_form(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()

            # Přiřadíme uživatele jako administrátora do tabulky project_user
            admin_role = role.objects.get(role_name='Administrator')
            project_user.objects.create(
                project=new_project,
                user=request.user,
                role=admin_role
            )

            # Přiřadíme základní kategorie (Frontend, Backend, etc.)
            basic_categories = ['Frontend', 'Backend', 'Database']
            for category_name in basic_categories:
                category.objects.create(
                    name=category_name,
                    project=new_project,  # Specifické pro tento projekt
                    description=f'Základní kategorie: {category_name}'
                )

            return redirect('index_project_cs')
    else:
        form = project_form()
    return render(request, 'project/new_project.html', {'form': form})




# View for deleting a project
def delete_project(request, project_id):
    project = get_object_or_404(project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'project/delete_project.html', {'project': project})



# View for editing an existing project
def edit_project(request, project_id):
    # Načtěte projekt, který se má upravit
    project_instance = get_object_or_404(project, pk=project_id)

    if request.method == 'POST':
        form = project_form(request.POST, instance=project_instance)
        if form.is_valid():
            form.save()
            return redirect('detail_project', project_id=project_instance.project_id)  # Přesměrování na detail projektu po úpravě
    else:
        form = project_form(instance=project_instance)

    return render(request, 'project/edit_project.html', {'form': form, 'project': project_instance})





@login_required
def index_project(request):
    # Načteme instanci uživatele podle jeho primárního klíče (ID)
    current_user = User.objects.get(pk=request.user.pk)
    # Vyhledáme projekty, kde je aktuální uživatel vlastníkem
    user_projects = project.objects.filter(owner=current_user).order_by('-created')
    return render(request, 'project/index_project.html', {'user_projects': user_projects})





@login_required
def detail_project(request, project_id):
    proj = get_object_or_404(project, pk=project_id)
    
    # Načteme úkoly a rozdělíme je do kategorií
    tasks_by_status = {
        'Ke zpracování': proj.tasks.filter(status='Ke zpracování'),
        'Probíhá': proj.tasks.filter(status='Probíhá'),
        'Hotovo': proj.tasks.filter(status='Hotovo')
    }

    # Načteme úkoly "Nice to have"
    nice_to_have_tasks = proj.tasks.filter(status='Nice to have')

    # Kontrola práv pro zobrazení kontaktů
    can_view_contacts = request.user.has_perm('project.view_contact') or request.user == proj.owner
    
    return render(request, 'project/detail_project.html', {
        'project': proj,
        'tasks_by_status': tasks_by_status,
        'nice_to_have_tasks': nice_to_have_tasks,
        'can_view_contacts': can_view_contacts,
    })





@login_required
def manage_project_users(request, project_id):
    project_instance = get_object_or_404(project, pk=project_id)
    members = project_user.objects.filter(project=project_instance)
    roles = role.objects.all()

    # Přidání nového uživatele
    if request.method == 'POST':
        form = add_user_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            role_instance = form.cleaned_data['role']
            project_user_instance, created = project_user.objects.get_or_create(user=user, project=project_instance)
            project_user_instance.role = role_instance
            project_user_instance.save()
            return redirect('manage_project_users', project_id=project_id)
    else:
        form = add_user_form()

    return render(request, 'project/manage_project_users.html', {
        'project': project_instance,
        'members': members,
        'roles': roles,
        'form': form
    })



@login_required
def remove_project_user(request, project_id, user_id):
    project_instance = get_object_or_404(project, pk=project_id)
    user_instance = get_object_or_404(User, pk=user_id)
    project_user_instance = get_object_or_404(project_user, project=project_instance, user=user_instance)
    project_user_instance.delete()
    return redirect('manage_project_users', project_id=project_id)



# # # T a s k s # # #
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




@login_required
def detail_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'project/detail_task.html', {'task': task})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = task_form(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('detail_project', project_id=task.project.project_id)
    else:
        form = task_form(instance=task)
    return render(request, 'project/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project_id = task.project.project_id
    task.delete()
    return redirect('detail_project', project_id=project_id)

@login_required
def update_task_status(request, task_id, status):
    task = get_object_or_404(Task, pk=task_id)
    task.status = status
    task.save()
    return redirect('detail_project', project_id=task.project.project_id)



# # # M i l e s t o n e s # # #@login_required
def create_milestone(request, project_id):
    proj = get_object_or_404(project, pk=project_id)
    
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            new_milestone = form.save(commit=False)
            new_milestone.project = proj
            new_milestone.save()
            return redirect('detail_project', project_id=proj.project_id)
    else:
        form = milestone_form()
    
    return render(request, 'project/create_milestone.html', {'form': form, 'project': proj})


### C A T E G O R Y ###
@login_required
def create_category(request, project_id):
    proj = get_object_or_404(project, pk=project_id)
    
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
    cat = get_object_or_404(category, pk=category_id)
    
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
    cat = get_object_or_404(category, pk=category_id)
    project_id = cat.project.project_id
    if request.method == 'POST':
        cat.delete()
        return redirect('detail_project', project_id=project_id)
    
    return render(request, 'project/delete_category.html', {'category': cat})
