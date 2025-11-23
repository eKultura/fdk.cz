# SWOT Analysis Views
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from fdk_cz.models import Organization, OrganizationMembership, Project, ProjectUser, SwotAnalysis


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

    return render(request, 'swot/list_swot.html', {
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
            return render(request, 'swot/create_swot.html', {
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

    return render(request, 'swot/create_swot.html', {
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

    return render(request, 'swot/detail_swot.html', {
        'swot': swot,
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

    return render(request, 'swot/edit_swot.html', {
        'swot': swot,
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

    return render(request, 'swot/delete_swot.html', {
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
