### views.index.py


from django.contrib.auth.decorators import login_required
from django.db.models import Count

from fdk_cz.models import  contact, project, task, test, test_result, user
from django.shortcuts import render




def index(request):
    # Načítání počtů pro úkoly dle statusů
    task_status_counts = task.objects.values('status').annotate(count=Count('status'))
    status_counts = {
        'Nezahájeno': 0,
        'Probíhá': 0,
        'Hotovo': 0,
    }
    # Přiřazení počtů k jednotlivým statusům
    for item in task_status_counts:
        status = item['status']
        if status in status_counts:
            status_counts[status] = item['count']

    total_tasks = sum(status_counts.values())

    # Načtení počtů pro různé typy dat
    total_projects = project.objects.count()
    open_tasks_count = task.objects.count()
    total_test_results = test.objects.count()
    total_users = user.objects.count()

    # Načtení prvních pěti uživatelových úkolů, projektů a kontaktů
    user_tasks = task.objects.filter(assigned=request.user).order_by('-due_date')[:5] if request.user.is_authenticated else None
    user_projects = project.objects.filter(project_users__user=request.user).distinct()[:5] if request.user.is_authenticated else None
    user_contacts = contact.objects.filter(account=request.user).distinct()[:5] if request.user.is_authenticated else None

    return render(request, 'index.html', {
        'status_counts': status_counts,
        'total_tasks': total_tasks, 
        'total_projects': total_projects,
        'open_tasks_count': open_tasks_count,
        'total_test_results': total_test_results,
        'total_users': total_users,
        'user_tasks': user_tasks,
        'user_projects': user_projects,
        'user_contacts': user_contacts,
    })



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





