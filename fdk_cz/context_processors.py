# fdk_cz/context_processors.py

from fdk_cz.models import UserModuleSubscription, Module, UserModulePreference, Organization, OrganizationMembership


def organization_context(request):
    """
    Context processor that provides current organization context and user's organizations
    """
    if not request.user.is_authenticated:
        return {
            'current_organization': None,
            'user_organizations': [],
            'is_personal_context': True
        }

    # Get all organizations user is member of
    memberships = OrganizationMembership.objects.filter(
        user=request.user
    ).select_related('organization')

    user_organizations = [m.organization for m in memberships]

    # Also include organizations user created
    created_orgs = Organization.objects.filter(created_by=request.user)
    for org in created_orgs:
        if org not in user_organizations:
            user_organizations.append(org)

    # Get current organization from session
    current_org_id = request.session.get('current_organization_id')
    current_organization = None

    if current_org_id:
        try:
            # Verify user has access to this organization
            org = Organization.objects.get(organization_id=current_org_id)
            if org in user_organizations:
                current_organization = org
            else:
                # User doesn't have access, clear session
                del request.session['current_organization_id']
        except Organization.DoesNotExist:
            # Invalid org id, clear session
            if 'current_organization_id' in request.session:
                del request.session['current_organization_id']

    return {
        'current_organization': current_organization,
        'user_organizations': user_organizations,
        'is_personal_context': current_organization is None
    }


def user_modules(request):
    """
    Context processor, který přidá user_has_module a visible_modules do každého template
    """
    if not request.user.is_authenticated:
        return {
            'user_has_module': {},
            'all_modules': [],
            'visible_modules': []
        }

    # Získat všechny aktivní moduly uživatele
    subscriptions = UserModuleSubscription.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('module')

    user_has_module = {
        sub.module.name: True
        for sub in subscriptions
    }

    # Free moduly má každý (přístup k funkcionalitě)
    user_has_module.update({
        'project_management': True,
        'task_management': True,
        'lists': True,
        'contacts': True
    })

    # Všechny moduly
    all_modules = Module.objects.filter(is_active=True).order_by('order')

    # Získat preferences uživatele
    user_prefs = {}
    for pref in UserModulePreference.objects.filter(user=request.user).select_related('module'):
        user_prefs[pref.module.module_id] = pref

    # Moduly viditelné v menu (respektuje UserModulePreference)
    # Menu zobrazuje moduly podle preference, přístup k funkcím kontroluje middleware
    visible_modules = []
    for module in all_modules:
        pref = user_prefs.get(module.module_id)

        if pref:
            # Uživatel má nastavenou preferenci - respektuj ji
            if pref.is_visible:
                visible_modules.append(module)
        else:
            # Žádná preference - použij default
            # Pouze projekty a úkoly jsou defaultně viditelné
            if module.name in ['project_management', 'task_management']:
                visible_modules.append(module)

    return {
        'user_has_module': user_has_module,
        'all_modules': all_modules,
        'visible_modules': visible_modules
    }
