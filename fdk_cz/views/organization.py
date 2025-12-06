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

    # Zkontrolovat VIP status
    try:
        from fdk_cz.models import UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        is_vip = user_profile.is_vip
        can_create_org = is_vip or request.user.is_superuser
    except:
        is_vip = False
        can_create_org = request.user.is_superuser

    context = {
        'owned_organizations': owned_orgs,
        'member_organizations': member_orgs,
        'can_create_org': can_create_org,
        'is_vip': is_vip,
    }
    return render(request, 'organization/dashboard.html', context)


@login_required
def create_organization(request):
    """Vytvoření nové organizace - pouze pro VIP uživatele"""

    # Získáme nebo vytvoříme profil uživatele
    try:
        from fdk_cz.models import UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        is_vip = user_profile.is_vip
        max_orgs = 3 if is_vip else 0  # Základní uživatelé nemohou vytvářet organizace
    except Exception as e:
        # Fallback pokud tabulka UserProfile neexistuje
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"UserProfile table doesn't exist yet: {e}")
        is_vip = False
        max_orgs = 0  # Výchozí = nelze vytvořit organizaci

    # Kontrola oprávnění - pouze VIP nebo superuser může vytvářet organizace
    if not is_vip and not request.user.is_superuser:
        messages.error(
            request,
            'Vytváření organizací je dostupné pouze pro VIP uživatele. '
            'Aktivujte VIP účet nebo požádejte administrátora o TEST roli.'
        )
        return redirect('organization_dashboard')

    # Kontrola limitu organizací pro uživatele už při GET požadavku
    existing_orgs_count = Organization.objects.filter(created_by=request.user).count()

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
            try:
                if user_profile.is_vip:
                    messages.error(request, f'Dosáhli jste maximálního počtu organizací ({max_orgs}) pro VIP uživatele.')
                else:
                    messages.error(request, 'Již máte vytvořenou jednu organizaci. Pro vytvoření dalších organizací (až 3) aktivujte VIP účet.')
            except:
                messages.error(request, f'Dosáhli jste maximálního počtu organizací ({max_orgs}).')
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

    # Zaměstnanci/členové nemohou sami sebe odebrat - pouze admin může odebrat ostatní
    if user_id == request.user.id:
        messages.error(request, 'Nemůžete sami sebe odebrat z organizace. O odebrání požádejte administrátora organizace.')
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
def set_current_organization(request, organization_id):
    """
    Set current organization context in session.
    """
    import logging
    logger = logging.getLogger(__name__)

    # Verify user has access to this organization
    org = get_object_or_404(Organization, pk=organization_id)

    # Check if user is member or creator
    is_member = OrganizationMembership.objects.filter(
        organization=org,
        user=request.user
    ).exists()

    if not is_member and org.created_by != request.user:
        messages.error(request, 'Nemáte přístup k této organizaci.')
        return redirect('organization_dashboard')

    # Save to session with extra logging
    request.session['current_organization_id'] = organization_id
    request.session.modified = True  # Force session save
    request.session.save()  # Explicitly save session

    # Verify it was saved
    saved_id = request.session.get('current_organization_id')
    logger.info(f"CONTEXT SWITCH: User {request.user.username} switched to org {org.name} (ID: {organization_id})")
    logger.info(f"CONTEXT SWITCH: Session key 'current_organization_id' = {saved_id}")
    logger.info(f"CONTEXT SWITCH: Session modified flag = {request.session.modified}")

    messages.success(request, f'🏢 Nyní jste v organizaci: {org.name}', extra_tags='persistent')

    # Redirect to organization dashboard to show the context
    return redirect('organization_dashboard')


@login_required
def set_personal_context(request):
    """
    Switch to personal context (remove organization from session).
    """
    import logging
    logger = logging.getLogger(__name__)

    # Remove organization from session
    if 'current_organization_id' in request.session:
        del request.session['current_organization_id']
        request.session.modified = True
        request.session.save()  # Explicitly save session

    logger.info(f"CONTEXT SWITCH: User {request.user.username} switched to personal context")
    messages.success(request, '👤 Nyní jste v osobním kontextu', extra_tags='persistent')

    # Redirect to dashboard
    return redirect('dashboard')


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
