# fdk_cz/context_processors.py

from fdk_cz.models import UserModuleSubscription, Module


def user_modules(request):
    """
    Context processor, který přidá user_has_module do každého template
    """
    if not request.user.is_authenticated:
        return {'user_has_module': {}, 'all_modules': []}

    # Získat všechny aktivní moduly uživatele
    subscriptions = UserModuleSubscription.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('module')

    user_has_module = {
        sub.module.name: True
        for sub in subscriptions
    }

    # Free moduly má každý
    user_has_module.update({
        'project_management': True,
        'task_management': True,
        'lists': True,
        'contacts': True
    })

    # Všechny moduly pro menu
    all_modules = Module.objects.filter(is_active=True).order_by('order')

    return {
        'user_has_module': user_has_module,
        'all_modules': all_modules
    }
