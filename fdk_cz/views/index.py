### views.index.py


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from fdk_cz.models import  contact, project, task, test, test_result, user



def index(request):
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