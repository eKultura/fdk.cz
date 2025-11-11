# -------------------------------------------------------------------
#                    VIEWS.USERS.PY
# -------------------------------------------------------------------
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from fdk_cz.forms.user import user_registration_form, profile_edit_form

from django.shortcuts import render, redirect

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  # přesměrování na index nebo dashboard
        else:
            messages.error(request, "Nesprávné uživatelské jméno nebo heslo.")  # Zobrazit chybovou zprávu
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})
    


def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
def user_profile(request):
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def user_settings(request):
    from fdk_cz.models import Module, UserModulePreference

    if request.method == 'POST':
        form = profile_edit_form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = profile_edit_form(instance=request.user)

    # Get all modules and user preferences
    modules = Module.objects.filter(is_active=True).order_by('order', 'display_name')
    user_preferences = {}
    for pref in UserModulePreference.objects.filter(user=request.user):
        user_preferences[pref.module_id] = pref

    # Prepare modules with their preference status
    modules_with_prefs = []
    default_visible_modules = ['project_management', 'task_management']
    for module in modules:
        pref = user_preferences.get(module.module_id)
        # Default: only project_management and task_management are visible
        default_visible = module.name in default_visible_modules
        modules_with_prefs.append({
            'module': module,
            'is_visible': pref.is_visible if pref else default_visible,
            'preference': pref
        })

    return render(request, 'user/settings.html', {
        'user': request.user,
        'form': form,
        'modules_with_prefs': modules_with_prefs
    })


@login_required
def toggle_module_visibility(request, module_id):
    """Toggle visibility of a module in the menu"""
    from fdk_cz.models import Module, UserModulePreference

    if request.method == 'POST':
        module = Module.objects.get(module_id=module_id)
        pref, created = UserModulePreference.objects.get_or_create(
            user=request.user,
            module=module
        )

        # Pokud byla preference právě vytvořena, je již is_visible=True (default)
        # Pokud již existuje, toggleneme ji
        if not created:
            pref.is_visible = not pref.is_visible
            pref.save()

        messages.success(request, f"Modul {module.display_name} byl {'zapnut' if pref.is_visible else 'vypnut'}.")

    # Redirect s fragment (kotva)
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    url = reverse('user_settings') + '#moduly'
    return HttpResponseRedirect(url)


def registration(request):
    if request.method == 'POST':
        form = user_registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # automatické přihlášení po registraci
            return redirect('index')  # Přesměrování po úspěšné registraci
    else:
        form = user_registration_form()
    return render(request, 'user/registration.html', {'form': form})






"""

def login(request):
    return render(request, 'user/login.html')

def logout(request):
    return render(request, 'user/logout.html')

def registration(request):
    return render(request, 'user/registration.html')

"""


