### views.index.py


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from fdk_cz.models import task, project, contact



def index(request):
    return render(request, 'index.html')




@login_required
def dashboard(request):
    # Načtení úkolů aktuálního uživatele
    user_tasks = task.objects.filter(assigned=request.user).order_by('-due_date')[:5]
    
    # Načtení projektů, na kterých uživatel pracuje nebo které vlastní
    user_projects = project.objects.filter(project_users__user=request.user).distinct()[:5]

    # Načtení kontaktů, které jsou sdílené nebo vlastněné uživatelem
    user_contacts = contact.objects.filter(account=request.user).distinct()[:5]

    return render(request, 'dashboard.html', {
        'user_tasks': user_tasks,
        'user_projects': user_projects,
        'user_contacts': user_contacts,
    })