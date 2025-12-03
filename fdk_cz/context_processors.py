# fdk_cz/context_processors.py

from fdk_cz.models import UserModuleSubscription, Module, UserModulePreference, Organization, OrganizationMembership


# Definice struktury menu pro celý systém
MENU_CONFIG = {
    'categories': [
        {
            'name': 'Management',
            'icon': '&#128295;',
            'modules': ['project_management', 'task_management', 'test_management', 'b2b_management',
                       'hr_management', 'risk_management', 'it_management', 'asset_management']
        },
        {
            'name': 'Finance',
            'icon': '&#128176;',
            'modules': ['accounting', 'grants']
        },
        {
            'name': 'Business',
            'icon': '&#129309;',
            'modules': ['contacts', 'contracts']
        },
        {
            'name': 'Nástroje',
            'icon': '&#128736;',
            'modules': ['lists', 'warehouse', 'law_ai', 'dms']
        },
    ],
    'modules': {
        'project_management': {
            'name': 'Správa projektů',
            'icon': '&#128295;',
            'url': 'index_project_cs',
            'url_prefixes': ['project', 'swot', 'gantt'],
            'submenu': [
                {'name': 'Seznam projektů', 'url': 'index_project_cs', 'icon': '&#128203;'},
                {'name': 'Nový projekt', 'url': 'create_project_cs', 'icon': '&#10133;'},
                {'name': 'SWOT analýzy', 'url': 'list_swot_analyses', 'icon': '&#128202;'},
                {'name': 'Ganttův diagram', 'url': 'gantt_chart', 'icon': '&#128197;'},
                {'name': 'Log aktivit', 'url': 'all_project_logs', 'icon': '&#128196;'},
                {'name': 'Nápověda', 'url': 'help_projects', 'icon': '&#10067;'},
            ]
        },
        'task_management': {
            'name': 'Správa úkolů',
            'icon': '&#10004;',
            'url': 'task_management',
            'url_prefixes': ['task'],
            'submenu': [
                {'name': 'Moje úkoly', 'url': 'task_management', 'icon': '&#128203;'},
                {'name': 'Nový úkol', 'url': 'create_task', 'icon': '&#10133;'},
                {'name': 'Nápověda', 'url': 'help_tasks', 'icon': '&#10067;'},
            ]
        },
        'test_management': {
            'name': 'Testování',
            'icon': '&#129514;',
            'url': 'list_tests',
            'url_prefixes': ['test'],
            'submenu': [
                {'name': 'Testy', 'url': 'list_tests', 'icon': '&#129514;'},
                {'name': 'Typy testů', 'url': 'list_test_types', 'icon': '&#128203;'},
                {'name': 'Scénáře', 'url': 'list_test_scenarios', 'icon': '&#128203;'},
                {'name': 'Chyby', 'url': 'list_bugs', 'icon': '&#128027;'},
                {'name': 'Nápověda', 'url': 'help_testing', 'icon': '&#10067;'},
            ]
        },
        'b2b_management': {
            'name': 'Správa B2B',
            'icon': '&#129309;',
            'url': 'b2b_dashboard',
            'url_prefixes': ['b2b'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'b2b_dashboard', 'icon': '&#128200;'},
                {'name': 'Nápověda', 'url': 'help_b2b', 'icon': '&#10067;'},
            ]
        },
        'hr_management': {
            'name': 'HR Management',
            'icon': '&#128188;',
            'url': 'hr_dashboard',
            'url_prefixes': ['hr'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'hr_dashboard', 'icon': '&#128200;'},
                {'name': 'Zaměstnanci', 'url': 'list_employees', 'icon': '&#128101;'},
                {'name': 'Oddělení', 'url': 'list_departments', 'icon': '&#127970;'},
                {'name': 'Nápověda', 'url': 'help_hr', 'icon': '&#10067;'},
            ]
        },
        'risk_management': {
            'name': 'Správa rizik',
            'icon': '&#9888;',
            'url': 'risk_dashboard',
            'url_prefixes': ['risk'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'risk_dashboard', 'icon': '&#128200;'},
                {'name': 'Seznam rizik', 'url': 'list_risks', 'icon': '&#128203;'},
                {'name': 'Nápověda', 'url': 'help_risks', 'icon': '&#10067;'},
            ]
        },
        'it_management': {
            'name': 'Správa IT',
            'icon': '&#128187;',
            'url': 'it_dashboard',
            'url_prefixes': ['it', 'incident'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'it_dashboard', 'icon': '&#128200;'},
                {'name': 'Incidenty', 'url': 'list_incidents', 'icon': '&#128680;'},
                {'name': 'Nápověda', 'url': 'help_it', 'icon': '&#10067;'},
            ]
        },
        'asset_management': {
            'name': 'Správa majetku',
            'icon': '&#128203;',
            'url': 'asset_dashboard',
            'url_prefixes': ['asset'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'asset_dashboard', 'icon': '&#128200;'},
                {'name': 'Seznam majetku', 'url': 'list_assets', 'icon': '&#128203;'},
                {'name': 'Nápověda', 'url': 'help_assets', 'icon': '&#10067;'},
            ]
        },
        'accounting': {
            'name': 'Účetnictví',
            'icon': '&#128202;',
            'url': 'accounting_dashboard',
            'url_prefixes': ['accounting', 'journal', 'ledger', 'chart_of_accounts'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'accounting_dashboard', 'icon': '&#128200;'},
                {'name': 'Účtová osnova', 'url': 'chart_of_accounts', 'icon': '&#128203;'},
                {'name': 'Deník', 'url': 'journal_list', 'icon': '&#128221;'},
                {'name': 'Nápověda', 'url': 'help_accounting', 'icon': '&#10067;'},
            ]
        },
        'grants': {
            'name': 'Granty & Dotace',
            'icon': '&#128176;',
            'url': 'grant_list',
            'url_prefixes': ['grant'],
            'submenu': [
                {'name': 'Seznam grantů', 'url': 'grant_list', 'icon': '&#128203;'},
                {'name': 'Nový grant', 'url': 'grant_create', 'icon': '&#10133;'},
                {'name': 'Nápověda', 'url': 'help_grants', 'icon': '&#10067;'},
            ]
        },
        'contacts': {
            'name': 'Kontakty',
            'icon': '&#128100;',
            'url': 'my_contacts',
            'url_prefixes': ['contact'],
            'submenu': [
                {'name': 'Moje kontakty', 'url': 'my_contacts', 'icon': '&#128203;'},
                {'name': 'Nový kontakt', 'url': 'create_contact', 'icon': '&#10133;'},
                {'name': 'Nápověda', 'url': 'help_contacts', 'icon': '&#10067;'},
            ]
        },
        'contracts': {
            'name': 'Smlouvy',
            'icon': '&#128196;',
            'url': 'list_contracts',
            'url_prefixes': ['contract'],
            'submenu': [
                {'name': 'Seznam smluv', 'url': 'list_contracts', 'icon': '&#128203;'},
                {'name': 'Nová smlouva', 'url': 'create_contract', 'icon': '&#10133;'},
                {'name': 'Nápověda', 'url': 'help_contracts', 'icon': '&#10067;'},
            ]
        },
        'lists': {
            'name': 'Seznamy',
            'icon': '&#128221;',
            'url': 'index_list',
            'url_prefixes': ['list'],
            'submenu': [
                {'name': 'Moje seznamy', 'url': 'index_list', 'icon': '&#128203;'},
                {'name': 'Nový seznam', 'url': 'create_list', 'icon': '&#10133;'},
                {'name': 'Nápověda', 'url': 'help_lists', 'icon': '&#10067;'},
            ]
        },
        'warehouse': {
            'name': 'Sklad',
            'icon': '&#128230;',
            'url': 'all_stores',
            'url_prefixes': ['store', 'warehouse'],
            'submenu': [
                {'name': 'Sklady', 'url': 'all_stores', 'icon': '&#128230;'},
                {'name': 'Nápověda', 'url': 'help_warehouse', 'icon': '&#10067;'},
            ]
        },
        'law_ai': {
            'name': 'AI Právník',
            'icon': '&#9889;',
            'url': 'pravo_ai',
            'url_prefixes': ['pravo', 'law'],
            'submenu': [
                {'name': 'AI Právník', 'url': 'pravo_ai', 'icon': '&#9889;'},
                {'name': 'Nápověda', 'url': 'help_law', 'icon': '&#10067;'},
            ]
        },
        'dms': {
            'name': 'DMS',
            'icon': '&#128193;',
            'url': 'dms_dashboard',
            'url_prefixes': ['dms', 'document'],
            'submenu': [
                {'name': 'Dashboard', 'url': 'dms_dashboard', 'icon': '&#128200;'},
                {'name': 'Dokumenty', 'url': 'dms_list', 'icon': '&#128203;'},
                {'name': 'Nápověda', 'url': 'help_dms', 'icon': '&#10067;'},
            ]
        },
    }
}


def get_active_module(request):
    """
    Detekuje aktivní modul na základě URL name
    """
    if not hasattr(request, 'resolver_match') or not request.resolver_match:
        return None

    url_name = request.resolver_match.url_name or ''

    # Projdi všechny moduly a najdi shodu
    for module_key, module_config in MENU_CONFIG['modules'].items():
        for prefix in module_config.get('url_prefixes', []):
            if url_name.startswith(prefix) or prefix in url_name:
                return module_key

    return None


def organization_context(request):
    """
    Context processor that provides current organization context and user's organizations
    """
    if not request.user.is_authenticated:
        return {
            'current_organization': None,
            'user_organizations': [],
            'is_personal_context': True,
            'can_switch_organizations': False
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

    # Check if user can switch organizations
    # Everyone can switch between personal and organization context
    # VIP users can have multiple organizations
    can_switch = len(user_organizations) > 0

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

    # Default to personal context (no automatic org selection)
    # Users explicitly choose organization or stay in personal context

    return {
        'current_organization': current_organization,
        'user_organizations': user_organizations,
        'is_personal_context': current_organization is None,
        'can_switch_organizations': can_switch
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

    # Získat aktivní modul pro menu
    active_module = get_active_module(request)

    # Zjistit, které kategorie mají viditelné moduly
    visible_module_names = {module.name for module in visible_modules}

    category_visibility = {}
    for category in MENU_CONFIG['categories']:
        has_visible_modules = any(
            module_name in visible_module_names
            for module_name in category['modules']
        )
        category_visibility[category['name']] = has_visible_modules

    return {
        'user_has_module': user_has_module,
        'all_modules': all_modules,
        'visible_modules': visible_modules,
        'menu_config': MENU_CONFIG,
        'active_module': active_module,
        'category_visibility': category_visibility,
    }
