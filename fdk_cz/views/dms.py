# -------------------------------------------------------------------
#                    VIEWS.DMS.PY
#                    Document Management System
# -------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from fdk_cz.models import ProjectDocument, Project, Organization


# -------------------------------------------------------------------
#                    DMS DASHBOARD
# -------------------------------------------------------------------

def dms_public(request):
    """
    Veřejný DMS dashboard - ukázkové/demo dokumenty pro anonymní uživatele
    """
    # Vzorové dokumenty pro demo účely
    sample_documents = [
        {
            'title': 'Projektová dokumentace XYZ',
            'document_type': 'Dokumentace',
            'project_name': 'Projekt XYZ',
            'organization_name': 'Demo Organizace s.r.o.',
            'uploaded_at': '15.11.2024',
        },
        {
            'title': 'Smlouva o spolupráci',
            'document_type': 'Smlouva',
            'project_name': 'Strategická spolupráce 2024',
            'organization_name': 'Partnerská firma a.s.',
            'uploaded_at': '10.11.2024',
        },
        {
            'title': 'Technická specifikace',
            'document_type': 'Specifikace',
            'project_name': 'Vývoj aplikace',
            'organization_name': 'Tech Company s.r.o.',
            'uploaded_at': '05.11.2024',
        },
        {
            'title': 'Zápisz jednání',
            'document_type': 'Zápis',
            'project_name': 'Měsíční review',
            'organization_name': 'Demo Organizace s.r.o.',
            'uploaded_at': '01.11.2024',
        },
    ]

    context = {
        'sample_documents': sample_documents,
        'is_demo': True,
    }
    return render(request, 'dms/dashboard.html', context)


@login_required
def dms_dashboard(request):
    """
    DMS dashboard pro přihlášené uživatele
    Zobrazuje dokumenty z projektů a organizací, kde je uživatel členem
    """
    # Získání organizací kde je uživatel členem nebo vlastníkem
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    # Získání projektů kde je uživatel členem nebo vlastníkem
    user_projects = Project.objects.filter(
        Q(organization__in=user_orgs) | Q(owner=request.user) | Q(project_users__user=request.user)
    ).distinct()

    # Získání všech dokumentů z těchto projektů
    documents = ProjectDocument.objects.filter(
        project__in=user_projects
    ).select_related('project', 'project__organization', 'uploaded_by').order_by('-uploaded_at')

    # Filtry
    project_filter = request.GET.get('project')
    if project_filter:
        documents = documents.filter(project_id=project_filter)

    org_filter = request.GET.get('organization')
    if org_filter:
        documents = documents.filter(project__organization_id=org_filter)

    doc_type_filter = request.GET.get('type')
    if doc_type_filter:
        documents = documents.filter(document_type__icontains=doc_type_filter)

    # Vyhledávání
    search = request.GET.get('search')
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(document_type__icontains=search)
        )

    context = {
        'documents': documents,
        'user_orgs': user_orgs,
        'user_projects': user_projects,
        'selected_project': project_filter,
        'selected_org': org_filter,
        'selected_type': doc_type_filter,
        'search_query': search,
        'is_demo': False,
    }
    return render(request, 'dms/dashboard.html', context)


@login_required
def dms_create_document(request):
    """
    Vytvoření nového dokumentu v DMS
    Uživatel může vybrat projekt ze svých projektů
    """
    # Získání projektů kde je uživatel členem
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    user_projects = Project.objects.filter(
        Q(organization__in=user_orgs) | Q(owner=request.user) | Q(project_users__user=request.user)
    ).distinct()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        title = request.POST.get('title')
        document_type = request.POST.get('document_type')
        description = request.POST.get('description')

        if project_id and title and document_type:
            project = get_object_or_404(Project, pk=project_id)

            # Ověření, že uživatel má přístup k projektu
            if project in user_projects:
                document = ProjectDocument.objects.create(
                    project=project,
                    title=title,
                    document_type=document_type,
                    description=description,
                    url='',  # Placeholder
                    file_path='',  # Placeholder
                    uploaded_by=request.user
                )
                messages.success(request, f'Dokument "{document.title}" byl úspěšně vytvořen.')
                return redirect('dms_dashboard')
            else:
                messages.error(request, 'Nemáte oprávnění vytvořit dokument v tomto projektu.')
        else:
            messages.error(request, 'Vyplňte všechna povinná pole.')

    context = {
        'user_projects': user_projects,
    }
    return render(request, 'dms/create_document.html', context)
