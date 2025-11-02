# -------------------------------------------------------------------
#                    VIEWS.B2B.PY
# -------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from fdk_cz.models import (
    B2BCompany, B2BContract, B2BDocument,
    Organization, Project
)
from fdk_cz.forms.b2b import (
    B2BCompanyForm, B2BContractForm, B2BDocumentForm
)

# -------------------------------------------------------------------
#                    B2B MANAGEMENT
# -------------------------------------------------------------------

@login_required
def b2b_dashboard(request):
    """Dashboard pro správu B2B vztahů"""
    # Get user's organizations
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    # Get companies
    companies = B2BCompany.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).annotate(
        contracts_count=Count('contracts')
    ).order_by('-created_at')[:10]

    # Get recent contracts
    recent_contracts = B2BContract.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).select_related('company', 'organization').order_by('-created_at')[:10]

    # Statistics
    total_companies = B2BCompany.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).count()

    total_contracts = B2BContract.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).count()

    active_contracts = B2BContract.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True),
        status='active'
    ).count()

    context = {
        'companies': companies,
        'recent_contracts': recent_contracts,
        'total_companies': total_companies,
        'total_contracts': total_contracts,
        'active_contracts': active_contracts,
    }
    return render(request, 'b2b/dashboard.html', context)


# -------------------------------------------------------------------
#                    B2B COMPANIES
# -------------------------------------------------------------------

@login_required
def list_companies(request):
    """Seznam B2B firem"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    companies = B2BCompany.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).annotate(
        contracts_count=Count('contracts')
    ).order_by('name')

    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        companies = companies.filter(category=category)

    # Search
    search = request.GET.get('search')
    if search:
        companies = companies.filter(
            Q(name__icontains=search) |
            Q(legal_name__icontains=search) |
            Q(company_id_number__icontains=search)
        )

    context = {
        'companies': companies,
        'category_choices': B2BCompany.CATEGORY_CHOICES,
        'selected_category': category,
        'search_query': search,
    }
    return render(request, 'b2b/list_companies.html', context)


@login_required
def create_company(request):
    """Vytvoření nové B2B firmy"""
    if request.method == 'POST':
        form = B2BCompanyForm(request.POST, user=request.user)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()
            messages.success(request, f'Firma "{company.name}" byla úspěšně vytvořena.')
            return redirect('list_b2b_companies')
    else:
        form = B2BCompanyForm(user=request.user)

    return render(request, 'b2b/create_company.html', {'form': form})


@login_required
def detail_company(request, company_id):
    """Detail B2B firmy"""
    company = get_object_or_404(B2BCompany, pk=company_id)

    # Get contracts for this company
    contracts = B2BContract.objects.filter(company=company).order_by('-created_at')

    # Get documents for this company
    documents = B2BDocument.objects.filter(company=company).order_by('-uploaded_at')

    context = {
        'company': company,
        'contracts': contracts,
        'documents': documents,
    }
    return render(request, 'b2b/detail_company.html', context)


@login_required
def edit_company(request, company_id):
    """Editace B2B firmy"""
    company = get_object_or_404(B2BCompany, pk=company_id)

    if request.method == 'POST':
        form = B2BCompanyForm(request.POST, instance=company, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Firma "{company.name}" byla úspěšně aktualizována.')
            return redirect('detail_b2b_company', company_id=company.company_id)
    else:
        form = B2BCompanyForm(instance=company, user=request.user)

    return render(request, 'b2b/edit_company.html', {'form': form, 'company': company})


@login_required
def delete_company(request, company_id):
    """Smazání B2B firmy"""
    company = get_object_or_404(B2BCompany, pk=company_id)

    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f'Firma "{company_name}" byla smazána.')
        return redirect('list_b2b_companies')

    return render(request, 'b2b/delete_company.html', {'company': company})


# -------------------------------------------------------------------
#                    B2B CONTRACTS
# -------------------------------------------------------------------

@login_required
def list_contracts(request):
    """Seznam B2B smluv"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    contracts = B2BContract.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).select_related('company', 'organization', 'project').order_by('-created_at')

    # Filter by status
    status = request.GET.get('status')
    if status:
        contracts = contracts.filter(status=status)

    # Search
    search = request.GET.get('search')
    if search:
        contracts = contracts.filter(
            Q(contract_number__icontains=search) |
            Q(title__icontains=search) |
            Q(company__name__icontains=search)
        )

    context = {
        'contracts': contracts,
        'status_choices': B2BContract.STATUS_CHOICES,
        'selected_status': status,
        'search_query': search,
    }
    return render(request, 'b2b/list_contracts.html', context)


@login_required
def create_contract(request):
    """Vytvoření nové B2B smlouvy"""
    if request.method == 'POST':
        form = B2BContractForm(request.POST, user=request.user)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.created_by = request.user
            contract.save()
            messages.success(request, f'Smlouva "{contract.contract_number}" byla úspěšně vytvořena.')
            return redirect('detail_b2b_contract', contract_id=contract.contract_id)
    else:
        form = B2BContractForm(user=request.user)

    return render(request, 'b2b/create_contract.html', {'form': form})


@login_required
def detail_contract(request, contract_id):
    """Detail B2B smlouvy"""
    contract = get_object_or_404(
        B2BContract.objects.select_related('company', 'organization', 'project'),
        pk=contract_id
    )

    # Get documents for this contract
    documents = B2BDocument.objects.filter(contract=contract).order_by('-uploaded_at')

    context = {
        'contract': contract,
        'documents': documents,
    }
    return render(request, 'b2b/detail_contract.html', context)


@login_required
def edit_contract(request, contract_id):
    """Editace B2B smlouvy"""
    contract = get_object_or_404(B2BContract, pk=contract_id)

    if request.method == 'POST':
        form = B2BContractForm(request.POST, instance=contract, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Smlouva "{contract.contract_number}" byla úspěšně aktualizována.')
            return redirect('detail_b2b_contract', contract_id=contract.contract_id)
    else:
        form = B2BContractForm(instance=contract, user=request.user)

    return render(request, 'b2b/edit_contract.html', {'form': form, 'contract': contract})


@login_required
def delete_contract(request, contract_id):
    """Smazání B2B smlouvy"""
    contract = get_object_or_404(B2BContract, pk=contract_id)

    if request.method == 'POST':
        contract_number = contract.contract_number
        contract.delete()
        messages.success(request, f'Smlouva "{contract_number}" byla smazána.')
        return redirect('list_b2b_contracts')

    return render(request, 'b2b/delete_contract.html', {'contract': contract})


# -------------------------------------------------------------------
#                    B2B DOCUMENTS (DMS Integration)
# -------------------------------------------------------------------

@login_required
def list_documents(request):
    """Seznam B2B dokumentů"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    documents = B2BDocument.objects.filter(
        Q(organization__in=user_orgs) | Q(organization__isnull=True)
    ).select_related('company', 'contract').order_by('-uploaded_at')

    # Filter by document type
    doc_type = request.GET.get('type')
    if doc_type:
        documents = documents.filter(document_type=doc_type)

    # Search
    search = request.GET.get('search')
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(keywords__icontains=search) |
            Q(categories__icontains=search)
        )

    context = {
        'documents': documents,
        'search_query': search,
        'selected_type': doc_type,
    }
    return render(request, 'b2b/list_documents.html', context)


@login_required
def create_document(request):
    """Nahrání nového B2B dokumentu"""
    if request.method == 'POST':
        form = B2BDocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, f'Dokument "{document.title}" byl úspěšně nahrán.')
            return redirect('list_b2b_documents')
    else:
        form = B2BDocumentForm(user=request.user)

    return render(request, 'b2b/create_document.html', {'form': form})


@login_required
def delete_document(request, document_id):
    """Smazání B2B dokumentu"""
    document = get_object_or_404(B2BDocument, pk=document_id)

    if request.method == 'POST':
        document_title = document.title
        document.delete()
        messages.success(request, f'Dokument "{document_title}" byl smazán.')
        return redirect('list_b2b_documents')

    return render(request, 'b2b/delete_document.html', {'document': document})
