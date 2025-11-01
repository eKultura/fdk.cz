# -------------------------------------------------------------------
#                    VIEWS.HR.PY
# -------------------------------------------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# -------------------------------------------------------------------
#                    HR MANAGEMENT
# -------------------------------------------------------------------

@login_required
def hr_dashboard(request):
    """Dashboard pro HR Management"""
    return render(request, 'hr/dashboard.html')


@login_required
def hr_employees(request):
    """Seznam zaměstnanců"""
    return render(request, 'hr/employees.html')


@login_required
def hr_attendance(request):
    """Docházka"""
    return render(request, 'hr/attendance.html')


@login_required
def hr_leave(request):
    """Dovolené a absence"""
    return render(request, 'hr/leave.html')