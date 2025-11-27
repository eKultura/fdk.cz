# -------------------------------------------------------------------
#                    VIEWS.RISK.PY
# -------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg

from fdk_cz.models import Risk, Project, Organization
from fdk_cz.forms.risk import RiskForm

# -------------------------------------------------------------------
#                    RISK MANAGEMENT
# -------------------------------------------------------------------

@login_required
def risk_dashboard(request):
    """Dashboard pro správu rizik"""
    # Get current organization context
    current_org_id = request.session.get('current_organization_id')

    # Build base query based on organization context
    if current_org_id:
        # Organization context: show only risks from this organization
        base_query = Q(organization_id=current_org_id) | Q(project__organization_id=current_org_id)
    else:
        # Personal context: show only risks without organization
        base_query = Q(organization__isnull=True, project__organization__isnull=True)

    # Get risks
    risks = Risk.objects.filter(
        base_query
    ).select_related('project', 'organization', 'owner').order_by('-risk_score', '-created_at')[:10]

    # Statistics
    total_risks = Risk.objects.filter(base_query).count()

    critical_risks = Risk.objects.filter(
        base_query,
        risk_score__gte=15  # High probability (4-5) * High impact (4-5)
    ).count()

    avg_risk_score = Risk.objects.filter(
        base_query
    ).aggregate(Avg('risk_score'))['risk_score__avg'] or 0

    # Risks by status
    risks_by_status = Risk.objects.filter(
        base_query
    ).values('status').annotate(count=Count('risk_id'))

    context = {
        'risks': risks,
        'total_risks': total_risks,
        'critical_risks': critical_risks,
        'avg_risk_score': round(avg_risk_score, 1),
        'risks_by_status': {item['status']: item['count'] for item in risks_by_status},
    }
    return render(request, 'risk/dashboard.html', context)


@login_required
def list_risks(request):
    """Seznam identifikovaných rizik"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    user_projects = Project.objects.filter(
        Q(owner=request.user) | Q(project_users__user=request.user)
    ).distinct()

    risks = Risk.objects.filter(
        Q(organization__in=user_orgs) | Q(project__in=user_projects)
    ).select_related('project', 'organization', 'owner').order_by('-risk_score', '-created_at')

    # Filter by status
    status = request.GET.get('status')
    if status:
        risks = risks.filter(status=status)

    # Filter by category
    category = request.GET.get('category')
    if category:
        risks = risks.filter(category=category)

    # Filter by project
    project_id = request.GET.get('project')
    if project_id:
        risks = risks.filter(project_id=project_id)

    # Search
    search = request.GET.get('search')
    if search:
        risks = risks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'risks': risks,
        'projects': user_projects,
        'status_choices': Risk.STATUS_CHOICES,
        'category_choices': Risk.CATEGORY_CHOICES,
        'selected_status': status,
        'selected_category': category,
        'selected_project': project_id,
        'search_query': search,
    }
    return render(request, 'risk/list_risks.html', context)


@login_required
def create_risk(request):
    """Vytvoření nového rizika"""
    if request.method == 'POST':
        form = RiskForm(request.POST, user=request.user)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.created_by = request.user
            risk.save()
            messages.success(request, f'Riziko "{risk.title}" bylo úspěšně vytvořeno.')
            return redirect('detail_risk', risk_id=risk.risk_id)
    else:
        form = RiskForm(user=request.user)

    return render(request, 'risk/create_risk.html', {'form': form})


@login_required
def detail_risk(request, risk_id):
    """Detail rizika"""
    risk = get_object_or_404(
        Risk.objects.select_related('project', 'organization', 'owner', 'created_by'),
        pk=risk_id
    )

    context = {
        'risk': risk,
    }
    return render(request, 'risk/detail_risk.html', context)


@login_required
def edit_risk(request, risk_id):
    """Editace rizika"""
    risk = get_object_or_404(Risk, pk=risk_id)

    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Riziko "{risk.title}" bylo úspěšně aktualizováno.')
            return redirect('detail_risk', risk_id=risk.risk_id)
    else:
        form = RiskForm(instance=risk, user=request.user)

    return render(request, 'risk/edit_risk.html', {'form': form, 'risk': risk})


@login_required
def delete_risk(request, risk_id):
    """Smazání rizika"""
    risk = get_object_or_404(Risk, pk=risk_id)

    if request.method == 'POST':
        risk_title = risk.title
        risk.delete()
        messages.success(request, f'Riziko "{risk_title}" bylo smazáno.')
        return redirect('list_risks')

    return render(request, 'risk/delete_risk.html', {'risk': risk})


@login_required
def risk_matrix(request):
    """Matice rizik (probability vs impact)"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    user_projects = Project.objects.filter(
        Q(owner=request.user) | Q(project_users__user=request.user)
    ).distinct()

    risks = Risk.objects.filter(
        Q(organization__in=user_orgs) | Q(project__in=user_projects)
    ).select_related('project', 'organization')

    # Group risks by probability and impact for matrix visualization
    matrix_data = {}
    for prob in range(1, 6):
        for imp in range(1, 6):
            matrix_data[f"{prob}_{imp}"] = risks.filter(probability=prob, impact=imp)

    context = {
        'risks': risks,
        'matrix_data': matrix_data,
    }
    return render(request, 'risk/risk_matrix.html', context)
