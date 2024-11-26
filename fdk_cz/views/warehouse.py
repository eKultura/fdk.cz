from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from fdk_cz.models import company, project, transaction, warehouse

from fdk_cz.forms.warehouse import transaction_form


#@login_required
def all_stores(request):
    stores = warehouse.objects.all()
    return render(request, 'warehouse/all_stores.html', {'stores': stores})

@login_required
def project_stores(request, project_id):
    project = get_object_or_404(project, pk=project_id)
    stores = project.stores.all()
    return render(request, 'warehouse/project_stores.html', {'stores': stores, 'project': project})

@login_required
def organization_stores(request, organization_id):
    organization = get_object_or_404(compmany, pk=organization_id)
    stores = organization.stores.all()
    return render(request, 'warehouse/organization_stores.html', {'stores': stores, 'organization': organization})

@login_required
def store_detail(request, store_id):
    store = get_object_or_404(warehouse, pk=store_id)
    return render(request, 'warehouse/store_detail.html', {'store': store})



# TRANSACTION

@login_required
def store_transactions(request, store_id):
    store = get_object_or_404(warehouse, pk=store_id)
    transactions = store.transactions.all()
    return render(request, 'warehouse/transactions.html', {'transactions': transactions, 'store': store})

@login_required
def create_transaction(request, store_id):
    store = get_object_or_404(warehouse, pk=store_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.store = store
            transaction.save()
            return redirect('store_transactions', store_id=store.id)
    else:
        form = TransactionForm()
    return render(request, 'warehouse/create_transaction.html', {'form': form, 'store': store})

@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(transaction, pk=transaction_id)
    return render(request, 'warehouse/transaction_detail.html', {'transaction': transaction})
