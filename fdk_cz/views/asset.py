# -------------------------------------------------------------------
#                    VIEWS.ASSET.PY
# -------------------------------------------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# -------------------------------------------------------------------
#                    ASSET MANAGEMENT
# -------------------------------------------------------------------

@login_required
def asset_dashboard(request):
    """Dashboard pro správu majetku"""
    return render(request, 'asset/dashboard.html')


@login_required
def asset_list(request):
    """Seznam majetku"""
    return render(request, 'asset/list.html')


@login_required
def asset_maintenance(request):
    """Údržba majetku"""
    return render(request, 'asset/maintenance.html')