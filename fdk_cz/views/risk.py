# -------------------------------------------------------------------
#                    VIEWS.RISK.PY
# -------------------------------------------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# -------------------------------------------------------------------
#                    RISK MANAGEMENT
# -------------------------------------------------------------------

@login_required
def risk_dashboard(request):
    """Dashboard pro správu rizik"""
    return render(request, 'risk/dashboard.html')


@login_required
def risk_list(request):
    """Seznam identifikovaných rizik"""
    return render(request, 'risk/list.html')


@login_required
def risk_matrix(request):
    """Matice rizik"""
    return render(request, 'risk/matrix.html')