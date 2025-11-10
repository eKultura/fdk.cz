# fdk_cz/context_processors.py

from fdk_cz.models import UserModuleSubscription, Module, UserModulePreference
import logging

logger = logging.getLogger(__name__)


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

    # DEBUG: Log module count
    module_count = Module.objects.count()
    logger.warning(f"DEBUG: Total modules in DB: {module_count}")

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
    logger.warning(f"DEBUG: Active modules: {all_modules.count()}")

    # Získat preferences uživatele
    user_prefs = {}
    for pref in UserModulePreference.objects.filter(user=request.user).select_related('module'):
        user_prefs[pref.module.module_id] = pref

    # Moduly viditelné v menu (respektuje UserModulePreference)
    visible_modules = []
    for module in all_modules:
        # Kontrola jestli má uživatel přístup k modulu
        if user_has_module.get(module.name, False):
            # Kontrola jestli má uživatel preference pro tento modul
            pref = user_prefs.get(module.module_id)

            # Defaultně viditelné jsou jen project_management a task_management
            if pref:
                # Uživatel má nastavenou preferenci
                if pref.is_visible:
                    visible_modules.append(module)
                    logger.warning(f"DEBUG: Module {module.name} visible (user pref)")
            else:
                # Žádná preference - použij default
                # Pouze projekty a úkoly jsou defaultně viditelné
                if module.name in ['project_management', 'task_management']:
                    visible_modules.append(module)
                    logger.warning(f"DEBUG: Module {module.name} visible (default)")

    logger.warning(f"DEBUG: Total visible modules: {len(visible_modules)}")

    return {
        'user_has_module': user_has_module,
        'all_modules': all_modules,
        'visible_modules': visible_modules
    }
