# -------------------------------------------------------------------
#                    VIEWS.ASSET.PY
# -------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum

from fdk_cz.models import Asset, AssetCategory, Organization
from fdk_cz.forms.asset import AssetForm, AssetCategoryForm

# -------------------------------------------------------------------
#                    ASSET MANAGEMENT
# -------------------------------------------------------------------

@login_required
def asset_dashboard(request):
    """Dashboard pro správu majetku"""
    # Get user's organizations
    user_orgs = Organization.objects.filter(
        Q(owner=request.user) | Q(organization_users__user=request.user)
    ).distinct()

    # Get assets
    assets = Asset.objects.filter(
        organization__in=user_orgs
    ).select_related('category', 'responsible_person').order_by('-created_at')[:10]

    # Statistics
    total_assets = Asset.objects.filter(organization__in=user_orgs).count()
    active_assets = Asset.objects.filter(organization__in=user_orgs, status='active').count()
    total_value = Asset.objects.filter(
        organization__in=user_orgs,
        status='active'
    ).aggregate(Sum('current_value'))['current_value__sum'] or 0

    # Assets by category
    categories_with_counts = AssetCategory.objects.filter(
        organization__in=user_orgs
    ).annotate(
        asset_count=Count('assets')
    ).order_by('-asset_count')[:5]

    context = {
        'assets': assets,
        'total_assets': total_assets,
        'active_assets': active_assets,
        'total_value': total_value,
        'categories_with_counts': categories_with_counts,
    }
    return render(request, 'asset/dashboard.html', context)


# -------------------------------------------------------------------
#                    ASSETS
# -------------------------------------------------------------------

@login_required
def list_assets(request):
    """Seznam majetku"""
    user_orgs = Organization.objects.filter(
        Q(owner=request.user) | Q(organization_users__user=request.user)
    ).distinct()

    assets = Asset.objects.filter(
        organization__in=user_orgs
    ).select_related('category', 'responsible_person', 'organization').order_by('name')

    # Filter by status
    status = request.GET.get('status')
    if status:
        assets = assets.filter(status=status)

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        assets = assets.filter(category_id=category_id)

    # Search
    search = request.GET.get('search')
    if search:
        assets = assets.filter(
            Q(name__icontains=search) |
            Q(asset_number__icontains=search) |
            Q(location__icontains=search)
        )

    categories = AssetCategory.objects.filter(organization__in=user_orgs)

    context = {
        'assets': assets,
        'categories': categories,
        'status_choices': Asset.STATUS_CHOICES,
        'selected_status': status,
        'selected_category': category_id,
        'search_query': search,
    }
    return render(request, 'asset/list_assets.html', context)


@login_required
def create_asset(request):
    """Vytvoření nového majetku"""
    if request.method == 'POST':
        form = AssetForm(request.POST, user=request.user)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'Majetek "{asset.name}" byl úspěšně vytvořen.')
            return redirect('detail_asset', asset_id=asset.asset_id)
    else:
        form = AssetForm(user=request.user)

    return render(request, 'asset/create_asset.html', {'form': form})


@login_required
def detail_asset(request, asset_id):
    """Detail majetku"""
    asset = get_object_or_404(
        Asset.objects.select_related('category', 'organization', 'responsible_person'),
        pk=asset_id
    )

    context = {
        'asset': asset,
    }
    return render(request, 'asset/detail_asset.html', context)


@login_required
def edit_asset(request, asset_id):
    """Editace majetku"""
    asset = get_object_or_404(Asset, pk=asset_id)

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Majetek "{asset.name}" byl úspěšně aktualizován.')
            return redirect('detail_asset', asset_id=asset.asset_id)
    else:
        form = AssetForm(instance=asset, user=request.user)

    return render(request, 'asset/edit_asset.html', {'form': form, 'asset': asset})


@login_required
def delete_asset(request, asset_id):
    """Smazání majetku"""
    asset = get_object_or_404(Asset, pk=asset_id)

    if request.method == 'POST':
        asset_name = asset.name
        asset.delete()
        messages.success(request, f'Majetek "{asset_name}" byl smazán.')
        return redirect('list_assets')

    return render(request, 'asset/delete_asset.html', {'asset': asset})


# -------------------------------------------------------------------
#                    ASSET CATEGORIES
# -------------------------------------------------------------------

@login_required
def list_categories(request):
    """Seznam kategorií majetku"""
    user_orgs = Organization.objects.filter(
        Q(owner=request.user) | Q(organization_users__user=request.user)
    ).distinct()

    categories = AssetCategory.objects.filter(
        organization__in=user_orgs
    ).annotate(
        asset_count=Count('assets')
    ).select_related('organization', 'parent_category').order_by('name')

    context = {
        'categories': categories,
    }
    return render(request, 'asset/list_categories.html', context)


@login_required
def create_category(request):
    """Vytvoření nové kategorie majetku"""
    if request.method == 'POST':
        form = AssetCategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Kategorie "{category.name}" byla úspěšně vytvořena.')
            return redirect('list_asset_categories')
    else:
        form = AssetCategoryForm(user=request.user)

    return render(request, 'asset/create_category.html', {'form': form})


@login_required
def edit_category(request, category_id):
    """Editace kategorie majetku"""
    category = get_object_or_404(AssetCategory, pk=category_id)

    if request.method == 'POST':
        form = AssetCategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Kategorie "{category.name}" byla úspěšně aktualizována.')
            return redirect('list_asset_categories')
    else:
        form = AssetCategoryForm(instance=category, user=request.user)

    return render(request, 'asset/edit_category.html', {'form': form, 'category': category})


@login_required
def delete_category(request, category_id):
    """Smazání kategorie majetku"""
    category = get_object_or_404(AssetCategory, pk=category_id)

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Kategorie "{category_name}" byla smazána.')
        return redirect('list_asset_categories')

    return render(request, 'asset/delete_category.html', {'category': category})
