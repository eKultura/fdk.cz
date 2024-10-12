
# VIEWS.CONTACT.py


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from fdk_cz.models import contract, project, User
from fdk_cz.forms.contract import contract_form




@login_required
def create_contract(request, project_id):
    project_instance = get_object_or_404(project, pk=project_id)
    
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
def list_contracts(request, project_id):
    project_instance = get_object_or_404(project, pk=project_id)
    contracts = contract.objects.filter(project=project_instance)
    
    return render(request, 'contract/list_contract.html', {'contracts': contracts, 'project': project_instance})



@login_required
def edit_contract(request, contract_id):
    contract_instance = get_object_or_404(contract, pk=contract_id)
    
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
    contract_instance = get_object_or_404(contract, pk=contract_id)
    
    return render(request, 'contract/detail_contract.html', {'contract': contract_instance})
