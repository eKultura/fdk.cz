# -------------------------------------------------------------------
#                    VIEWS.IT.PY
# -------------------------------------------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# -------------------------------------------------------------------
#                    IT MANAGEMENT
# -------------------------------------------------------------------

@login_required
def it_dashboard(request):
    """Dashboard pro správu IT"""
    return render(request, 'it/dashboard.html')


@login_required
def it_assets(request):
    """IT aktiva"""
    return render(request, 'it/assets.html')


@login_required
def it_tickets(request):
    """IT tickety"""
    return render(request, 'it/tickets.html')


@login_required
def it_licenses(request):
    """Správa licencí"""
    return render(request, 'it/licenses.html')