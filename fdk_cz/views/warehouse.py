# -------------------------------------------------------------------
#                    VIEWS.WAREHOUSE.PY
# -------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from fdk_cz.models import Company, Project, Warehouse, WarehouseTransaction, WarehouseItem, WarehouseCategory

from fdk_cz.forms.warehouse import transaction_form, WarehouseForm, WarehouseItemForm, WarehouseCategoryForm

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------


#@login_required
def all_stores(request):
    stores = Warehouse.objects.all()
    return render(request, 'warehouse/all_stores.html', {'stores': stores})

@login_required
def project_stores(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    stores = project.stores.all()
    return render(request, 'warehouse/project_stores.html', {'stores': stores, 'project': project})

@login_required
def organization_stores(request, organization_id):
    from fdk_cz.models import Organization
    organization = get_object_or_404(Organization, pk=organization_id)
    stores = organization.stores.all()
    return render(request, 'warehouse/organization_stores.html', {'stores': stores, 'organization': organization})

@login_required
def store_detail(request, store_id):
    store = get_object_or_404(Warehouse, pk=store_id)
    return render(request, 'warehouse/store_detail.html', {'store': store})



# TRANSACTION

@login_required
def store_transactions(request, store_id):
    store = get_object_or_404(Warehouse, pk=store_id)
    transactions = store.transactions.all()
    return render(request, 'warehouse/transactions.html', {'transactions': transactions, 'store': store})

@login_required
def create_transaction(request, store_id):
    store = get_object_or_404(Warehouse, pk=store_id)
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
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render(request, 'warehouse/transaction_detail.html', {'transaction': transaction})


# CREATE WAREHOUSE

@login_required
def create_warehouse(request):
    """Create a new warehouse"""
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, f'Sklad "{warehouse.name}" byl úspěšně vytvořen.')
            return redirect('store_detail', store_id=warehouse.warehouse_id)
    else:
        form = WarehouseForm()

    return render(request, 'warehouse/create_warehouse.html', {'form': form})


@login_required
def create_warehouse_for_project(request, project_id):
    """Create a new warehouse for a specific project"""
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.project = project
            warehouse.save()
            messages.success(request, f'Sklad "{warehouse.name}" byl úspěšně vytvořen pro projekt {project.name}.')
            return redirect('project_stores', project_id=project.project_id)
    else:
        form = WarehouseForm(initial={'project': project})

    return render(request, 'warehouse/create_warehouse.html', {
        'form': form,
        'project': project,
        'for_project': True
    })


@login_required
def create_warehouse_for_organization(request, organization_id):
    """Create a new warehouse for a specific organization"""
    from fdk_cz.models import Organization
    organization = get_object_or_404(Organization, pk=organization_id)

    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.organization = organization
            warehouse.save()
            messages.success(request, f'Sklad "{warehouse.name}" byl úspěšně vytvořen pro organizaci {organization.name}.')
            return redirect('organization_stores', organization_id=organization.organization_id)
    else:
        form = WarehouseForm(initial={'organization': organization})

    return render(request, 'warehouse/create_warehouse.html', {
        'form': form,
        'organization': organization,
        'for_organization': True
    })


# CREATE WAREHOUSE ITEM

@login_required
def create_warehouse_item(request, store_id):
    """Add a new item to a warehouse"""
    store = get_object_or_404(Warehouse, pk=store_id)

    if request.method == 'POST':
        form = WarehouseItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.warehouse = store
            item.save()
            messages.success(request, f'Položka "{item.name}" byla úspěšně přidána do skladu.')
            return redirect('store_detail', store_id=store.warehouse_id)
    else:
        form = WarehouseItemForm()

    return render(request, 'warehouse/create_item.html', {
        'form': form,
        'store': store
    })


# CREATE WAREHOUSE CATEGORY

@login_required
def create_warehouse_category(request):
    """Create a new warehouse category"""
    if request.method == 'POST':
        form = WarehouseCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Kategorie "{category.name}" byla úspěšně vytvořena.')
            return redirect('all_stores')
    else:
        form = WarehouseCategoryForm()

    return render(request, 'warehouse/create_category.html', {'form': form})


@login_required
def list_warehouse_categories(request):
    """List all warehouse categories"""
    categories = WarehouseCategory.objects.all()
    return render(request, 'warehouse/list_categories.html', {'categories': categories})
