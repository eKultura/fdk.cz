"""
Views pro správu organizací
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from fdk_cz.models import Organization, OrganizationMembership, User, OrganizationRole, ModuleRole


@login_required
def organization_dashboard(request):
    """Dashboard organizací uživatele"""
    # Organizace, které uživatel vytvořil
    owned_orgs = Organization.objects.filter(created_by=request.user)

    # Organizace, kde je uživatel členem
    member_orgs = Organization.objects.filter(members=request.user).exclude(created_by=request.user)

    context = {
        'owned_organizations': owned_orgs,
        'member_organizations': member_orgs,
    }
    return render(request, 'organization/dashboard.html', context)


@login_required
def create_organization(request):
    """Vytvoření nové organizace"""
    if request.method == 'POST':
        name = request.POST.get('name')
        ico = request.POST.get('ico')

        if not name or not ico:
            messages.error(request, 'Vyplňte prosím název a IČO organizace.')
            return render(request, 'organization/create.html')

        # Kontrola, zda IČO již není použito
        if Organization.objects.filter(ico=ico).exists():
            messages.error(request, 'Organizace s tímto IČO již existuje.')
            return render(request, 'organization/create.html', {'name': name, 'ico': ico})

        # Vytvoření organizace
        org = Organization.objects.create(
            name=name,
            ico=ico,
            created_by=request.user
        )

        # Přidání tvůrce jako admin
        OrganizationMembership.objects.create(
            user=request.user,
            organization=org,
            role='admin'
        )

        messages.success(request, f'Organizace "{name}" byla úspěšně vytvořena.')
        return redirect('organization_detail', organization_id=org.organization_id)

    return render(request, 'organization/create.html')


@login_required
def organization_detail(request, organization_id):
    """Detail organizace"""
    org = get_object_or_404(Organization, pk=organization_id)

    # Kontrola přístupu
    is_member = OrganizationMembership.objects.filter(
        organization=org,
        user=request.user
    ).exists()

    if not is_member and org.created_by != request.user:
        messages.error(request, 'Nemáte přístup k této organizaci.')
        return redirect('organization_dashboard')

    # Získání členů
    memberships = OrganizationMembership.objects.filter(
        organization=org
    ).select_related('user')

    context = {
        'organization': org,
        'memberships': memberships,
        'is_admin': org.created_by == request.user or OrganizationMembership.objects.filter(
            organization=org,
            user=request.user,
            role='admin'
        ).exists()
    }
    return render(request, 'organization/detail.html', context)


@login_required
def search_users(request):
    """AJAX endpoint pro vyhledávání uživatelů"""
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'users': []})

    # Vyhledej uživatele podle emailu nebo jména
    users = User.objects.filter(
        Q(email__icontains=query) |
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )[:10]  # Limit na 10 výsledků

    results = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.get_full_name() or user.username
    } for user in users]

    return JsonResponse({'users': results})


@login_required
def add_member(request, organization_id):
    """Přidání člena do organizace"""
    org = get_object_or_404(Organization, pk=organization_id)

    # Kontrola, zda je uživatel admin
    is_admin = org.created_by == request.user or OrganizationMembership.objects.filter(
        organization=org,
        user=request.user,
        role='admin'
    ).exists()

    if not is_admin:
        messages.error(request, 'Nemáte oprávnění přidávat členy.')
        return redirect('organization_detail', organization_id=organization_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role', 'member')

        try:
            user = User.objects.get(pk=user_id)

            # Kontrola, zda už není členem
            if OrganizationMembership.objects.filter(organization=org, user=user).exists():
                messages.warning(request, f'Uživatel {user.username} již je členem organizace.')
            else:
                OrganizationMembership.objects.create(
                    organization=org,
                    user=user,
                    role=role
                )
                messages.success(request, f'Uživatel {user.username} byl přidán do organizace.')
        except User.DoesNotExist:
            messages.error(request, 'Uživatel nenalezen.')

    return redirect('organization_detail', organization_id=organization_id)


@login_required
def remove_member(request, organization_id, user_id):
    """Odebrání člena z organizace"""
    org = get_object_or_404(Organization, pk=organization_id)

    # Kontrola, zda je uživatel admin
    is_admin = org.created_by == request.user or OrganizationMembership.objects.filter(
        organization=org,
        user=request.user,
        role='admin'
    ).exists()

    if not is_admin:
        messages.error(request, 'Nemáte oprávnění odebírat členy.')
        return redirect('organization_detail', organization_id=organization_id)

    try:
        membership = OrganizationMembership.objects.get(
            organization=org,
            user_id=user_id
        )

        # Nelze odebrat tvůrce organizace
        if org.created_by.id == user_id:
            messages.error(request, 'Nelze odebrat tvůrce organizace.')
        else:
            username = membership.user.username
            membership.delete()
            messages.success(request, f'Uživatel {username} byl odebrán z organizace.')
    except OrganizationMembership.DoesNotExist:
        messages.error(request, 'Člen nenalezen.')

    return redirect('organization_detail', organization_id=organization_id)


@login_required
def set_current_organization(request, organization_id=None):
    """
    Set current organization context in session.
    If organization_id is None, sets to personal context.
    """
    if organization_id is None:
        # Switch to personal context
        if 'current_organization_id' in request.session:
            del request.session['current_organization_id']
        messages.success(request, 'Přepnuto na osobní kontext.')
    else:
        # Verify user has access to this organization
        org = get_object_or_404(Organization, pk=organization_id)

        # Check if user is member or creator
        is_member = OrganizationMembership.objects.filter(
            organization=org,
            user=request.user
        ).exists()

        if not is_member and org.created_by != request.user:
            messages.error(request, 'Nemáte přístup k této organizaci.')
            return redirect('index')

        request.session['current_organization_id'] = organization_id
        messages.success(request, f'Přepnuto na organizaci: {org.name}')

    # Redirect back to previous page or index
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


@login_required
def organization_iam(request, organization_id):
    """IAM správa organizace - role a oprávnění"""
    org = get_object_or_404(Organization, pk=organization_id)

    # Kontrola přístupu
    is_member = OrganizationMembership.objects.filter(
        organization=org,
        user=request.user
    ).exists()

    if not is_member and org.created_by != request.user:
        messages.error(request, 'Nemáte přístup k této organizaci.')
        return redirect('organization_dashboard')

    # Kontrola, zda je uživatel admin
    is_admin = org.created_by == request.user or OrganizationMembership.objects.filter(
        organization=org,
        user=request.user,
        role='admin'
    ).exists()

    # Získat všechny role organizace
    org_roles = OrganizationRole.objects.filter(
        organization=org
    ).select_related('membership__user').prefetch_related('permissions')

    # Získat všechny modulové role
    module_roles = ModuleRole.objects.filter(
        organization=org
    ).select_related('membership__user', 'module').prefetch_related('permissions')

    # Členové s jejich rolemi
    memberships = OrganizationMembership.objects.filter(
        organization=org
    ).select_related('user').prefetch_related('organization_roles', 'module_roles')

    context = {
        'organization': org,
        'is_admin': is_admin,
        'memberships': memberships,
        'org_roles': org_roles,
        'module_roles': module_roles,
    }
    return render(request, 'organization/iam.html', context)


@login_required
def change_member_role(request, organization_id, user_id):
    """Změna základní role člena (admin/member/viewer)"""
    org = get_object_or_404(Organization, pk=organization_id)

    # Kontrola, zda je uživatel admin
    is_admin = org.created_by == request.user or OrganizationMembership.objects.filter(
        organization=org,
        user=request.user,
        role='admin'
    ).exists()

    if not is_admin:
        messages.error(request, 'Nemáte oprávnění měnit role.')
        return redirect('organization_detail', organization_id=organization_id)

    if request.method == 'POST':
        new_role = request.POST.get('role')

        if new_role not in ['admin', 'member', 'viewer']:
            messages.error(request, 'Neplatná role.')
            return redirect('organization_iam', organization_id=organization_id)

        try:
            membership = OrganizationMembership.objects.get(
                organization=org,
                user_id=user_id
            )

            # Nelze změnit roli tvůrce organizace
            if org.created_by.id == user_id:
                messages.error(request, 'Nelze změnit roli tvůrce organizace.')
            else:
                old_role = membership.role
                membership.role = new_role
                membership.save()
                messages.success(request, f'Role uživatele {membership.user.username} změněna z {old_role} na {new_role}.')
        except OrganizationMembership.DoesNotExist:
            messages.error(request, 'Člen nenalezen.')

    return redirect('organization_iam', organization_id=organization_id)
