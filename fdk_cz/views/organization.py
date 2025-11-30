"""
Views pro správu organizací
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.db import transaction
from fdk_cz.models import Organization, OrganizationMembership, User, OrganizationRole, ModuleRole, ModuleAccess


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
    # Kontrola limitu organizací pro uživatele už při GET požadavku
    existing_orgs_count = Organization.objects.filter(created_by=request.user).count()
    max_orgs = 1  # Aktuálně je povolena 1 organizace na uživatele (lze rozšířit o VIP logiku)

    if request.method == 'POST':
        name = request.POST.get('name')
        ico = request.POST.get('ico')

        if not name or not ico:
            messages.error(request, 'Vyplňte prosím název a IČO organizace.')
            return render(request, 'organization/create.html', {
                'existing_orgs_count': existing_orgs_count,
                'max_orgs': max_orgs
            })

        # Kontrola limitu organizací pro uživatele
        if existing_orgs_count >= max_orgs:
            messages.error(request, 'Již máte vytvořenou jednu organizaci. Pro vytvoření další organizace je potřeba VIP účet.')
            return redirect('organization_dashboard')

        # Kontrola, zda IČO již není použito
        if Organization.objects.filter(ico=ico).exists():
            messages.error(request, 'Organizace s tímto IČO již existuje.')
            return render(request, 'organization/create.html', {
                'name': name,
                'ico': ico,
                'existing_orgs_count': existing_orgs_count,
                'max_orgs': max_orgs
            })

        # Použít transakci pro atomické vytvoření organizace a členství
        try:
            with transaction.atomic():
                # Vytvoření organizace
                org = Organization.objects.create(
                    name=name,
                    ico=ico,
                    created_by=request.user
                )

                # Přidání tvůrce jako admin
                admin_role = OrganizationRole.objects.get(role_name='organization_admin')
                OrganizationMembership.objects.create(
                    user=request.user,
                    organization=org,
                    role=admin_role
                )

            messages.success(request, f'Organizace "{name}" byla úspěšně vytvořena.')
            return redirect('organization_detail', organization_id=org.organization_id)
        except OrganizationRole.DoesNotExist:
            messages.error(request, 'Systémová chyba: Role "organization_admin" neexistuje v databázi. Kontaktujte administrátora.')
            return render(request, 'organization/create.html', {
                'name': name,
                'ico': ico,
                'existing_orgs_count': existing_orgs_count,
                'max_orgs': max_orgs
            })

    return render(request, 'organization/create.html', {
        'existing_orgs_count': existing_orgs_count,
        'max_orgs': max_orgs
    })


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
            role__role_name='organization_admin'
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
        role__role_name='organization_admin'
    ).exists()

    if not is_admin:
        messages.error(request, 'Nemáte oprávnění přidávat členy.')
        return redirect('organization_detail', organization_id=organization_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role', 'organization_member')

        try:
            user = User.objects.get(pk=user_id)

            # Kontrola, zda už není členem
            if OrganizationMembership.objects.filter(organization=org, user=user).exists():
                messages.warning(request, f'Uživatel {user.username} již je členem organizace.')
            else:
                # Získat objekt role podle jména
                role_obj = OrganizationRole.objects.get(role_name=role)
                OrganizationMembership.objects.create(
                    organization=org,
                    user=user,
                    role=role_obj
                )
                messages.success(request, f'Uživatel {user.username} byl přidán do organizace.')
        except User.DoesNotExist:
            messages.error(request, 'Uživatel nenalezen.')
        except OrganizationRole.DoesNotExist:
            messages.error(request, f'Role "{role}" neexistuje v databázi.')

    return redirect('organization_detail', organization_id=organization_id)


@login_required
def remove_member(request, organization_id, user_id):
    """Odebrání člena z organizace"""
    org = get_object_or_404(Organization, pk=organization_id)

    # Kontrola, zda je uživatel admin
    is_admin = org.created_by == request.user or OrganizationMembership.objects.filter(
        organization=org,
        user=request.user,
        role__role_name='organization_admin'
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
        role__role_name='organization_admin'
    ).exists()

    # Členové s jejich rolemi
    memberships = OrganizationMembership.objects.filter(
        organization=org
    ).select_related('user', 'role').prefetch_related('role__permissions')

    # Modulové přístupy pro organizaci
    module_accesses = ModuleAccess.objects.filter(
        organization=org,
        project__isnull=True  # Pouze přístupy na úrovni organizace
    ).select_related('user', 'role').prefetch_related('role__permissions')

    context = {
        'organization': org,
        'is_admin': is_admin,
        'memberships': memberships,
        'org_roles': [],  # Prozatím prázdné - pro budoucí rozšíření
        'module_roles': module_accesses,
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
        role__role_name='organization_admin'
    ).exists()

    if not is_admin:
        messages.error(request, 'Nemáte oprávnění měnit role.')
        return redirect('organization_detail', organization_id=organization_id)

    if request.method == 'POST':
        new_role_name = request.POST.get('role')

        if new_role_name not in ['organization_admin', 'organization_member', 'organization_viewer']:
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
                # Najít objekt role podle jména
                new_role = OrganizationRole.objects.get(role_name=new_role_name)
                old_role_name = membership.role.role_name
                membership.role = new_role
                membership.save()
                messages.success(request, f'Role uživatele {membership.user.username} změněna z {old_role_name} na {new_role_name}.')
        except OrganizationMembership.DoesNotExist:
            messages.error(request, 'Člen nenalezen.')
        except OrganizationRole.DoesNotExist:
            messages.error(request, f'Role "{new_role_name}" neexistuje v databázi.')

    return redirect('organization_iam', organization_id=organization_id)
