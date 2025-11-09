# -------------------------------------------------------------------
#                    VIEWS.CONTRACT.PY
# -------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from fdk_cz.models import Contract, Project, User
from fdk_cz.forms.contract import contract_form

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------


@login_required
def create_contract(request, project_id):
    project_instance = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = contract_form(request.POST, request.FILES)
        if form.is_valid():
            new_contract = form.save(commit=False)
            new_contract.project = project_instance
            new_contract.save()
            return redirect('detail_project', project_id=project_id)
    else:
        form = contract_form()

    return render(request, 'contract/create_contract.html', {'form': form, 'project': project_instance})




@login_required
def list_contracts(request, project_id=None):
    """Seznam smluv - buď všechny uživatele nebo pro konkrétní projekt"""
    from django.db.models import Q

    if project_id:
        project_instance = get_object_or_404(Project, pk=project_id)
        contracts = Contract.objects.filter(project=project_instance)
        user_projects = None
    else:
        # Všechny smlouvy uživatele napříč projekty kde je členem
        user_projects = Project.objects.filter(
            Q(owner=request.user) | Q(project_users__user=request.user)
        ).distinct()
        contracts = Contract.objects.filter(project__in=user_projects).select_related('project')
        project_instance = None

    return render(request, 'contract/list_contract.html', {
        'contracts': contracts,
        'project': project_instance,
        'user_projects': user_projects
    })



@login_required
def edit_contract(request, contract_id):
    contract_instance = get_object_or_404(Contract, pk=contract_id)
    
    if request.method == 'POST':
        form = contract_form(request.POST, request.FILES, instance=contract_instance)
        if form.is_valid():
            form.save()
            return redirect('detail_project', project_id=contract_instance.project.project_id)
    else:
        form = contract_form(instance=contract_instance)

    return render(request, 'contract/edit_contract.html', {'form': form, 'contract': contract_instance})



@login_required
def detail_contract(request, contract_id):
    contract_instance = get_object_or_404(Contract, pk=contract_id)
    
    return render(request, 'contract/detail_contract.html', {'contract': contract_instance})
