# -------------------------------------------------------------------
#                    VIEWS.B2B.PY
# -------------------------------------------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# -------------------------------------------------------------------
#                    B2B MANAGEMENT
# -------------------------------------------------------------------

@login_required
def b2b_dashboard(request):
    """Dashboard pro správu B2B vztahů"""
    return render(request, 'b2b/dashboard.html')


@login_required
def b2b_clients(request):
    """Seznam B2B klientů"""
    return render(request, 'b2b/clients.html')


@login_required
def b2b_opportunities(request):
    """Obchodní příležitosti"""
    return render(request, 'b2b/opportunities.html')