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
    test_types = TestType.objects.filter(Project_id=project_id)
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
    from django.utils import timezone

    error_instance = get_object_or_404(TestError, pk=error_id)
    project_id = error_instance.project.project_id  # Získání ID projektu pro přesměrování
    if request.method == 'POST':
        # Soft delete - mark as deleted instead of physically deleting
        error_instance.deleted = True
        error_instance.deleted_by = request.user
        error_instance.deleted_at = timezone.now()
        error_instance.save()
        return redirect('detail_project', project_id=project_id)  # Přesměrování na detail projektu
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
    test_instance = get_object_or_404(test, pk=test_id)
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
    test_results = test_result.objects.filter(project__in=user_projects)
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
    test_errors_list = TestError.objects.filter(project__in=user_projects).exclude(deleted=True).order_by('-date_created')

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

