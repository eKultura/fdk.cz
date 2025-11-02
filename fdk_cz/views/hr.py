# -------------------------------------------------------------------
#                    VIEWS.HR.PY
# -------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from fdk_cz.models import Employee, Department, Organization, User
from fdk_cz.forms.hr import EmployeeForm, DepartmentForm

# -------------------------------------------------------------------
#                    HR MANAGEMENT
# -------------------------------------------------------------------

@login_required
def hr_dashboard(request):
    """Dashboard pro HR Management"""
    # Get user's organizations
    user_orgs = Organization.objects.filter(
        Q(owner=request.user) | Q(organization_users__user=request.user)
    ).distinct()

    # Get employees
    employees = Employee.objects.filter(
        organization__in=user_orgs
    ).select_related('department', 'user').order_by('-created_at')[:10]

    # Statistics
    total_employees = Employee.objects.filter(organization__in=user_orgs).count()
    active_employees = Employee.objects.filter(organization__in=user_orgs, status='active').count()
    total_departments = Department.objects.filter(organization__in=user_orgs).count()

    # Employees by department
    departments_with_counts = Department.objects.filter(
        organization__in=user_orgs
    ).annotate(
        employee_count=Count('employees')
    ).order_by('-employee_count')[:5]

    context = {
        'employees': employees,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'total_departments': total_departments,
        'departments_with_counts': departments_with_counts,
    }
    return render(request, 'hr/dashboard.html', context)


# -------------------------------------------------------------------
#                    EMPLOYEES
# -------------------------------------------------------------------

@login_required
def list_employees(request):
    """Seznam zaměstnanců"""
    user_orgs = Organization.objects.filter(
        Q(owner=request.user) | Q(organization_users__user=request.user)
    ).distinct()

    employees = Employee.objects.filter(
        organization__in=user_orgs
    ).select_related('department', 'user', 'organization').order_by('last_name', 'first_name')

    # Filter by status
    status = request.GET.get('status')
    if status:
        employees = employees.filter(status=status)

    # Filter by department
    department_id = request.GET.get('department')
    if department_id:
        employees = employees.filter(department_id=department_id)

    # Search
    search = request.GET.get('search')
    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(employee_number__icontains=search)
        )

    departments = Department.objects.filter(organization__in=user_orgs)

    context = {
        'employees': employees,
        'departments': departments,
        'status_choices': Employee.STATUS_CHOICES,
        'selected_status': status,
        'selected_department': department_id,
        'search_query': search,
    }
    return render(request, 'hr/list_employees.html', context)


@login_required
def create_employee(request):
    """Vytvoření nového zaměstnance"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST, user=request.user)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Zaměstnanec "{employee.get_full_name()}" byl úspěšně vytvořen.')
            return redirect('list_employees')
    else:
        form = EmployeeForm(user=request.user)

    return render(request, 'hr/create_employee.html', {'form': form})


@login_required
def detail_employee(request, employee_id):
    """Detail zaměstnance - karta zaměstnance"""
    employee = get_object_or_404(
        Employee.objects.select_related('department', 'user', 'organization'),
        pk=employee_id
    )

    context = {
        'employee': employee,
    }
    return render(request, 'hr/detail_employee.html', context)


@login_required
def edit_employee(request, employee_id):
    """Editace zaměstnance"""
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zaměstnanec "{employee.get_full_name()}" byl úspěšně aktualizován.')
            return redirect('detail_employee', employee_id=employee.employee_id)
    else:
        form = EmployeeForm(instance=employee, user=request.user)

    return render(request, 'hr/edit_employee.html', {'form': form, 'employee': employee})


@login_required
def delete_employee(request, employee_id):
    """Smazání zaměstnance"""
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        employee_name = employee.get_full_name()
        employee.delete()
        messages.success(request, f'Zaměstnanec "{employee_name}" byl smazán.')
        return redirect('list_employees')

    return render(request, 'hr/delete_employee.html', {'employee': employee})


# -------------------------------------------------------------------
#                    DEPARTMENTS
# -------------------------------------------------------------------

@login_required
def list_departments(request):
    """Seznam oddělení"""
    user_orgs = Organization.objects.filter(
        Q(owner=request.user) | Q(organization_users__user=request.user)
    ).distinct()

    departments = Department.objects.filter(
        organization__in=user_orgs
    ).annotate(
        employee_count=Count('employees')
    ).select_related('organization', 'manager', 'parent_department').order_by('name')

    context = {
        'departments': departments,
    }
    return render(request, 'hr/list_departments.html', context)


@login_required
def create_department(request):
    """Vytvoření nového oddělení"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST, user=request.user)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Oddělení "{department.name}" bylo úspěšně vytvořeno.')
            return redirect('list_departments')
    else:
        form = DepartmentForm(user=request.user)

    return render(request, 'hr/create_department.html', {'form': form})


@login_required
def detail_department(request, department_id):
    """Detail oddělení"""
    department = get_object_or_404(
        Department.objects.select_related('organization', 'manager', 'parent_department'),
        pk=department_id
    )

    # Get employees in this department
    employees = Employee.objects.filter(department=department).select_related('user')

    context = {
        'department': department,
        'employees': employees,
    }
    return render(request, 'hr/detail_department.html', context)


@login_required
def edit_department(request, department_id):
    """Editace oddělení"""
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Oddělení "{department.name}" bylo úspěšně aktualizováno.')
            return redirect('detail_department', department_id=department.department_id)
    else:
        form = DepartmentForm(instance=department, user=request.user)

    return render(request, 'hr/edit_department.html', {'form': form, 'department': department})


@login_required
def delete_department(request, department_id):
    """Smazání oddělení"""
    department = get_object_or_404(Department, pk=department_id)

    if request.method == 'POST':
        department_name = department.name
        department.delete()
        messages.success(request, f'Oddělení "{department_name}" bylo smazáno.')
        return redirect('list_departments')

    return render(request, 'hr/delete_department.html', {'department': department})
