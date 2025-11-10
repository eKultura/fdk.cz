# fdk_cz/context_processors.py

from fdk_cz.models import UserModuleSubscription, Module, UserModulePreference


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

    # DEBUG: Print to stdout (visible in nohup.out)
    module_count = Module.objects.count()
    print(f"🔍 DEBUG context_processors: Total modules in DB: {module_count}")

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

    print(f"🔍 DEBUG: user_has_module = {user_has_module}")

    # Všechny moduly
    all_modules = Module.objects.filter(is_active=True).order_by('order')
    print(f"🔍 DEBUG: Active modules count: {all_modules.count()}")

    # Print all module names
    for m in all_modules:
        print(f"   - Module: {m.name} (id={m.module_id}, display={m.display_name})")

    # Získat preferences uživatele
    user_prefs = {}
    for pref in UserModulePreference.objects.filter(user=request.user).select_related('module'):
        user_prefs[pref.module.module_id] = pref
        print(f"🔍 DEBUG: User pref for {pref.module.name}: visible={pref.is_visible}")

    # Moduly viditelné v menu (respektuje UserModulePreference)
    visible_modules = []
    for module in all_modules:
        print(f"🔍 DEBUG: Checking module {module.name}...")

        # Kontrola jestli má uživatel přístup k modulu
        has_access = user_has_module.get(module.name, False)
        print(f"   - Has access: {has_access}")

        if has_access:
            # Kontrola jestli má uživatel preference pro tento modul
            pref = user_prefs.get(module.module_id)
            print(f"   - Preference: {pref}")

            # Defaultně viditelné jsou jen project_management a task_management
            if pref:
                # Uživatel má nastavenou preferenci
                if pref.is_visible:
                    visible_modules.append(module)
                    print(f"   ✅ Module {module.name} VISIBLE (user pref)")
                else:
                    print(f"   ❌ Module {module.name} HIDDEN (user pref)")
            else:
                # Žádná preference - použij default
                # Pouze projekty a úkoly jsou defaultně viditelné
                if module.name in ['project_management', 'task_management']:
                    visible_modules.append(module)
                    print(f"   ✅ Module {module.name} VISIBLE (default)")
                else:
                    print(f"   ⚪ Module {module.name} HIDDEN (default, no pref)")
        else:
            print(f"   ❌ Module {module.name} - NO ACCESS")

    print(f"🔍 DEBUG: Total visible modules: {len(visible_modules)}")
    for m in visible_modules:
        print(f"   ✅ {m.name}")

    return {
        'user_has_module': user_has_module,
        'all_modules': all_modules,
        'visible_modules': visible_modules
    }
