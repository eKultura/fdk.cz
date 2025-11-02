# -------------------------------------------------------------------
#                    VIEWS.IT.PY
# -------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from fdk_cz.models import ITAsset, ITIncident, Organization
from fdk_cz.forms.it import ITAssetForm, ITIncidentForm

# -------------------------------------------------------------------
#                    IT MANAGEMENT
# -------------------------------------------------------------------

@login_required
def it_dashboard(request):
    """Dashboard pro správu IT"""
    # Get user's organizations
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    # Get IT assets
    assets = ITAsset.objects.filter(
        organization__in=user_orgs
    ).select_related('assigned_to').order_by('-created_at')[:10]

    # Get recent incidents
    incidents = ITIncident.objects.filter(
        organization__in=user_orgs
    ).select_related('affected_asset', 'assigned_to').order_by('-reported_at')[:10]

    # Statistics
    total_assets = ITAsset.objects.filter(organization__in=user_orgs).count()
    active_assets = ITAsset.objects.filter(organization__in=user_orgs, status='active').count()
    total_incidents = ITIncident.objects.filter(organization__in=user_orgs).count()
    open_incidents = ITIncident.objects.filter(
        organization__in=user_orgs,
        status__in=['new', 'assigned', 'in_progress']
    ).count()

    context = {
        'assets': assets,
        'incidents': incidents,
        'total_assets': total_assets,
        'active_assets': active_assets,
        'total_incidents': total_incidents,
        'open_incidents': open_incidents,
    }
    return render(request, 'it/dashboard.html', context)


# -------------------------------------------------------------------
#                    IT ASSETS
# -------------------------------------------------------------------

@login_required
def list_assets(request):
    """Seznam IT aktiv"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    assets = ITAsset.objects.filter(
        organization__in=user_orgs
    ).select_related('assigned_to', 'organization').order_by('name')

    # Filter by asset type
    asset_type = request.GET.get('type')
    if asset_type:
        assets = assets.filter(asset_type=asset_type)

    # Filter by status
    status = request.GET.get('status')
    if status:
        assets = assets.filter(status=status)

    # Search
    search = request.GET.get('search')
    if search:
        assets = assets.filter(
            Q(name__icontains=search) |
            Q(asset_tag__icontains=search) |
            Q(serial_number__icontains=search)
        )

    context = {
        'assets': assets,
        'asset_type_choices': ITAsset.ASSET_TYPE_CHOICES,
        'status_choices': ITAsset.STATUS_CHOICES,
        'selected_type': asset_type,
        'selected_status': status,
        'search_query': search,
    }
    return render(request, 'it/list_assets.html', context)


@login_required
def create_asset(request):
    """Vytvoření nového IT aktiva"""
    if request.method == 'POST':
        form = ITAssetForm(request.POST, user=request.user)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'IT aktivum "{asset.name}" bylo úspěšně vytvořeno.')
            return redirect('detail_it_asset', asset_id=asset.asset_id)
    else:
        form = ITAssetForm(user=request.user)

    return render(request, 'it/create_asset.html', {'form': form})


@login_required
def detail_asset(request, asset_id):
    """Detail IT aktiva"""
    asset = get_object_or_404(
        ITAsset.objects.select_related('organization', 'assigned_to'),
        pk=asset_id
    )

    # Get incidents for this asset
    incidents = ITIncident.objects.filter(affected_asset=asset).order_by('-reported_at')

    context = {
        'asset': asset,
        'incidents': incidents,
    }
    return render(request, 'it/detail_asset.html', context)


@login_required
def edit_asset(request, asset_id):
    """Editace IT aktiva"""
    asset = get_object_or_404(ITAsset, pk=asset_id)

    if request.method == 'POST':
        form = ITAssetForm(request.POST, instance=asset, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'IT aktivum "{asset.name}" bylo úspěšně aktualizováno.')
            return redirect('detail_it_asset', asset_id=asset.asset_id)
    else:
        form = ITAssetForm(instance=asset, user=request.user)

    return render(request, 'it/edit_asset.html', {'form': form, 'asset': asset})


@login_required
def delete_asset(request, asset_id):
    """Smazání IT aktiva"""
    asset = get_object_or_404(ITAsset, pk=asset_id)

    if request.method == 'POST':
        asset_name = asset.name
        asset.delete()
        messages.success(request, f'IT aktivum "{asset_name}" bylo smazáno.')
        return redirect('list_it_assets')

    return render(request, 'it/delete_asset.html', {'asset': asset})


# -------------------------------------------------------------------
#                    IT INCIDENTS (ITIL)
# -------------------------------------------------------------------

@login_required
def list_incidents(request):
    """Seznam IT incidentů (ITIL Incident Management)"""
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    incidents = ITIncident.objects.filter(
        organization__in=user_orgs
    ).select_related('affected_asset', 'reported_by', 'assigned_to').order_by('-reported_at')

    # Filter by status
    status = request.GET.get('status')
    if status:
        incidents = incidents.filter(status=status)

    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        incidents = incidents.filter(priority=priority)

    # Search
    search = request.GET.get('search')
    if search:
        incidents = incidents.filter(
            Q(title__icontains=search) |
            Q(incident_number__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'incidents': incidents,
        'status_choices': ITIncident.STATUS_CHOICES,
        'priority_choices': ITIncident.PRIORITY_CHOICES,
        'selected_status': status,
        'selected_priority': priority,
        'search_query': search,
    }
    return render(request, 'it/list_incidents.html', context)


@login_required
def create_incident(request):
    """Vytvoření nového IT incidentu"""
    if request.method == 'POST':
        form = ITIncidentForm(request.POST, user=request.user)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()
            messages.success(request, f'Incident "{incident.incident_number}" byl úspěšně vytvořen.')
            return redirect('detail_it_incident', incident_id=incident.incident_id)
    else:
        form = ITIncidentForm(user=request.user)

    return render(request, 'it/create_incident.html', {'form': form})


@login_required
def detail_incident(request, incident_id):
    """Detail IT incidentu"""
    incident = get_object_or_404(
        ITIncident.objects.select_related('organization', 'affected_asset', 'reported_by', 'assigned_to'),
        pk=incident_id
    )

    context = {
        'incident': incident,
    }
    return render(request, 'it/detail_incident.html', context)


@login_required
def edit_incident(request, incident_id):
    """Editace IT incidentu"""
    incident = get_object_or_404(ITIncident, pk=incident_id)

    if request.method == 'POST':
        form = ITIncidentForm(request.POST, instance=incident, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Incident "{incident.incident_number}" byl úspěšně aktualizován.')
            return redirect('detail_it_incident', incident_id=incident.incident_id)
    else:
        form = ITIncidentForm(instance=incident, user=request.user)

    return render(request, 'it/edit_incident.html', {'form': form, 'incident': incident})


@login_required
def delete_incident(request, incident_id):
    """Smazání IT incidentu"""
    incident = get_object_or_404(ITIncident, pk=incident_id)

    if request.method == 'POST':
        incident_number = incident.incident_number
        incident.delete()
        messages.success(request, f'Incident "{incident_number}" byl smazán.')
        return redirect('list_it_incidents')

    return render(request, 'it/delete_incident.html', {'incident': incident})
