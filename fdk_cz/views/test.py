# -------------------------------------------------------------------
#                    VIEWS.TEST.PY
# -------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from fdk_cz.forms.test import test_type_form, test_form, test_result_form, test_error_form
from fdk_cz.models import TestType, Test, TestResult, TestError, Project

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------

@login_required
def get_test_types(request, project_id):
    test_types = TestType.objects.filter(project_id=project_id)
    data = {'test_types': [{'id': test_type.test_type_id, 'name': test_type.name} for test_type in test_types]}
    return JsonResponse(data)
@login_required
def get_test_results(request, project_id):
    try:
        project_id = int(project_id)
        test_results = TestResult.objects.filter(project_id=project_id)
        data = {'test_results': [{'id': result.pk, 'name': result.result} for result in test_results]}
        return JsonResponse(data)
    except ValueError:
        return JsonResponse({'error': 'Neplatné ID projektu'}, status=400)



@login_required
def delete_test_error(request, error_id):
    error_instance = get_object_or_404(TestError, pk=error_id)
    project_id = error_instance.project.project_id
    if request.method == 'POST':
        # Soft delete
        error_instance.deleted = True
        error_instance.save()
        return redirect('detail_project', project_id=project_id)
    return render(request, 'test/delete_test_error.html', {'error': error_instance})



# Typy testů - výpis
@login_required
def list_test_types(request):
    user_projects = Project.objects.filter(project_users__user=request.user)
    test_types = TestType.objects.filter(project__in=user_projects)
    return render(request, 'test/list_test_types.html', {'test_types': test_types, 'projects': user_projects})

# Přidání nového typu testu
@login_required
def create_test_type(request):
    if request.method == 'POST':
        form = test_type_form(request.POST, user=request.user)  # Předáme uživatele do formuláře
        if form.is_valid():
            form.save()
            return redirect('list_test_types')
    else:
        form = test_type_form(user=request.user)  # Předáme uživatele do formuláře
    return render(request, 'test/create_test_type.html', {'form': form})


# Editace typu testu
@login_required
def edit_test_type(request, test_type_id):
    test_type_instance = get_object_or_404(TestType, pk=test_type_id)

    if request.method == 'POST':
        form = test_type_form(request.POST, instance=test_type_instance, user=request.user)  # Předáváme 'user' při POST
        if form.is_valid():
            form.save()
            return redirect('list_test_types')
    else:
        form = test_type_form(instance=test_type_instance, user=request.user)  # Předáváme 'user' při GET

    return render(request, 'test/edit_test_type.html', {'form': form, 'test_type': test_type_instance})





# Výpis testů
@login_required
def list_tests(request):
    user_projects = Project.objects.filter(project_users__user=request.user)
    tests = Test.objects.filter(project__in=user_projects)
    test_types = TestType.objects.filter(project__in=user_projects)
    test_errors = TestError.objects.filter(status='open', project__in=user_projects).exclude(deleted=True).order_by('-date_created')[:10]

    return render(request, 'test/list_tests.html', {
        'tests': tests,
        'test_types': test_types,
        'test_errors': test_errors,
        'projects': user_projects
    })





# Přidání nového testu
@login_required
def create_test(request):
    if request.method == 'POST':
        form = test_form(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_tests')
    else:
        form = test_form(user=request.user)
    return render(request, 'test/create_test.html', {'form': form})



# Editace testu
@login_required
def edit_test(request, test_id):
    test_instance = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        form = test_form(request.POST, instance=test_instance, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_test')
    else:
        form = test_form(instance=test_instance, user=request.user)
    return render(request, 'test/edit_test.html', {'form': form, 'test': test_instance})





# Výpis výsledků testů
@login_required
def list_test_results(request):
    user_projects = Project.objects.filter(project_users__user=request.user)
    test_results = TestResult.objects.filter(project__in=user_projects)
    return render(request, 'test/list_test_results.html', {'test_results': test_results, 'projects': user_projects})

# Přidání nového výsledku testu
@login_required
def create_test_result(request):
    if request.method == 'POST':
        form = test_result_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_test_results')
    else:
        form = test_result_form()
    return render(request, 'test/create_test_result.html', {'form': form})



# Výpis chyb
@login_required
def list_test_errors(request):
    from django.core.paginator import Paginator

    user_projects = Project.objects.filter(project_users__user=request.user)
    test_errors_list = TestError.objects.filter(project__in=user_projects).exclude(deleted=True).exclude(status='closed').order_by('-date_created')

    # Pagination
    paginator = Paginator(test_errors_list, 20)  # Show 20 errors per page
    page_number = request.GET.get('page')
    test_errors = paginator.get_page(page_number)

    return render(request, 'test/list_test_errors.html', {
        'test_errors': test_errors,
        'projects': user_projects,
        'is_paginated': test_errors.has_other_pages(),
        'page_obj': test_errors
    })




# Přidání nové chyby
@login_required
def create_test_error(request, project_id=None):
    """Vytvoření nové testovací chyby, s možností přednastavení projektu"""
    initial_data = {}
    if project_id:
        initial_data['project'] = project_id

    if request.method == 'POST':
        form = test_error_form(request.POST, user=request.user)
        if form.is_valid():
            new_error = form.save(commit=False)
            new_error.created_by = request.user
            # Pokud byl projekt přednastavený a disabled, nastavit ho ručně
            if project_id and not new_error.project:
                new_error.project_id = project_id
            new_error.save()
            # Přesměrování na detail projektu
            return redirect('detail_project', project_id=new_error.project.project_id)
    else:
        form = test_error_form(initial=initial_data, user=request.user)

    context = {
        'form': form,
        'preselected_project_id': project_id,
    }
    return render(request, 'test/create_test_error.html', context)





@login_required
def edit_test_error(request, test_error_id):
    test_error_instance = get_object_or_404(TestError, pk=test_error_id)
    if request.method == 'POST':
        form = test_error_form(request.POST, instance=test_error_instance, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_test_errors')
    else:
        form = test_error_form(instance=test_error_instance, user=request.user)
    return render(request, 'test/edit_test_error.html', {'form': form, 'test_error': test_error_instance})



@login_required
def detail_test_error(request, test_error_id):
    error = get_object_or_404(TestError, pk=test_error_id)
    return render(request, 'test/detail_test_error.html', {'error': error})


@login_required
def mark_error_fixed(request, test_error_id):
    """Označit chybu jako opravenou (změní status na 'closed')"""
    error = get_object_or_404(TestError, pk=test_error_id)
    error.status = 'closed'
    error.save()
    return redirect('detail_test_error', test_error_id=test_error_id)


# -------------------------------------------------------------------
#                    TEST SCENARIOS
# -------------------------------------------------------------------

@login_required
def list_test_scenarios(request):
    """Seznam testovacích scénářů"""
    from django.db.models import Q
    from fdk_cz.models import Organization, TestScenario
    
    # Získat organizace uživatele
    user_orgs = Organization.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()
    
    # Získat projekty uživatele
    user_projects = Project.objects.filter(project_users__user=request.user)
    
    # Filtrovat scénáře podle trojjediného kontextu
    scenarios = TestScenario.objects.filter(
        Q(organization__in=user_orgs) |  # Organizační
        Q(project__in=user_projects) |   # Projektové
        Q(owner=request.user)             # Osobní
    ).select_related('organization', 'project', 'owner', 'created_by').distinct().order_by('-created_at')
    
    # Filtrování podle statusu
    status = request.GET.get('status')
    if status:
        scenarios = scenarios.filter(status=status)
    
    # Filtrování podle priority
    priority = request.GET.get('priority')
    if priority:
        scenarios = scenarios.filter(priority=priority)
    
    # Vyhledávání
    search = request.GET.get('search')
    if search:
        scenarios = scenarios.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(steps__icontains=search)
        )
    
    context = {
        'scenarios': scenarios,
        'status_choices': TestScenario.STATUS_CHOICES,
        'priority_choices': TestScenario.PRIORITY_CHOICES,
        'selected_status': status,
        'selected_priority': priority,
        'search_query': search,
    }
    return render(request, 'test/list_scenarios.html', context)


@login_required
def create_test_scenario(request):
    """Vytvoření nového testovacího scénáře"""
    from fdk_cz.forms.test import TestScenarioForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = TestScenarioForm(request.POST, user=request.user)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.created_by = request.user
            scenario.save()
            messages.success(request, f'Scénář "{scenario.name}" byl úspěšně vytvořen.')
            return redirect('list_test_scenarios')
    else:
        form = TestScenarioForm(user=request.user)
    
    return render(request, 'test/create_scenario.html', {'form': form})


@login_required
def detail_test_scenario(request, scenario_id):
    """Detail testovacího scénáře"""
    from fdk_cz.models import TestScenario
    
    scenario = get_object_or_404(
        TestScenario.objects.select_related('organization', 'project', 'owner', 'created_by'),
        pk=scenario_id
    )
    
    context = {
        'scenario': scenario,
    }
    return render(request, 'test/detail_scenario.html', context)


@login_required
def edit_test_scenario(request, scenario_id):
    """Editace testovacího scénáře"""
    from fdk_cz.models import TestScenario
    from fdk_cz.forms.test import TestScenarioForm
    from django.contrib import messages
    
    scenario = get_object_or_404(TestScenario, pk=scenario_id)
    
    if request.method == 'POST':
        form = TestScenarioForm(request.POST, instance=scenario, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Scénář "{scenario.name}" byl úspěšně aktualizován.')
            return redirect('detail_test_scenario', scenario_id=scenario.scenario_id)
    else:
        form = TestScenarioForm(instance=scenario, user=request.user)
    
    return render(request, 'test/edit_scenario.html', {'form': form, 'scenario': scenario})


@login_required
def delete_test_scenario(request, scenario_id):
    """Smazání testovacího scénáře"""
    from fdk_cz.models import TestScenario
    from django.contrib import messages
    
    scenario = get_object_or_404(TestScenario, pk=scenario_id)
    
    if request.method == 'POST':
        scenario_name = scenario.name
        scenario.delete()
        messages.success(request, f'Scénář "{scenario_name}" byl smazán.')
        return redirect('list_test_scenarios')
    
    return render(request, 'test/delete_scenario.html', {'scenario': scenario})
