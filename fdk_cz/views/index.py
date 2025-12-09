# -------------------------------------------------------------------
#                    VIEWS.INDEX.PY
# -------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Count, Q

from fdk_cz.models import  Contact, Project, ProjectTask, ProjectDocument, Test, TestResult, User
from django.shortcuts import render

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------


def index(request):
    # Načítání počtů pro úkoly dle statusů
    task_status_counts = ProjectTask.objects.values('status').annotate(count=Count('status'))
    status_counts = {
        'Nezahájeno': 0,
        'Probíhá': 0,
        'Hotovo': 0,
    }
    user = request.user if request.user.is_authenticated else None
    # Přiřazení počtů k jednotlivým statusům
    for item in task_status_counts:
        status = item['status']
        if status in status_counts:
            status_counts[status] = item['count']

    total_tasks = sum(status_counts.values())

    # Načtení počtů pro různé typy dat
    total_projects = Project.objects.count()
    open_tasks_count = ProjectTask.objects.count()
    total_test_results = Test.objects.count()
    total_users = User.objects.count()

    # Načtení prvních pěti uživatelových úkolů, projektů a kontaktů
    user_tasks = ProjectTask.objects.filter(assigned=request.user).order_by('-due_date')[:5] if request.user.is_authenticated else None
    user_projects = Project.objects.filter(project_users__user=request.user).distinct()[:5] if request.user.is_authenticated else None
    user_contacts = Contact.objects.filter(account=request.user).distinct()[:5] if request.user.is_authenticated else None

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
    # Načtení úkolů aktuálního uživatele (BEZ hotových úkolů)
    user_tasks = ProjectTask.objects.filter(
        assigned=request.user
    ).exclude(
        status='Hotovo'  # Vyloučit hotové úkoly z dashboardu
    ).order_by('-due_date')[:5]

    # Načtení projektů, na kterých uživatel pracuje nebo které vlastní
    user_projects = Project.objects.filter(project_users__user=request.user).distinct()[:5]

    # Načtení kontaktů, které jsou sdílené nebo vlastněné uživatelem
    user_contacts = Contact.objects.filter(account=request.user).distinct()[:5]

    return render(request, 'dashboard.html', {
        'user_tasks': user_tasks,
        'user_projects': user_projects,
        'user_contacts': user_contacts,
    })


@login_required
def global_search(request):
    """
    Globální vyhledávání napříč projekty, úkoly a dokumenty
    """
    query = request.GET.get('q', '').strip()

    # Inicializace prázdných výsledků
    projects = []
    tasks = []
    documents = []

    if query and len(query) >= 2:
        # Filtr pouze na projekty/úkoly/dokumenty, ke kterým má uživatel přístup

        # Vyhledávání projektů (vlastní nebo je členem)
        projects = Project.objects.filter(
            Q(project_users__user=request.user) | Q(owner=request.user)
        ).filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()[:10]

        # Vyhledávání úkolů (přiřazené nebo v projektech, kde je členem)
        tasks = ProjectTask.objects.filter(
            Q(assigned=request.user) | Q(project__project_users__user=request.user)
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()[:15]

        # Vyhledávání dokumentů (v projektech, kde je členem)
        documents = ProjectDocument.objects.filter(
            Q(project__project_users__user=request.user) | Q(project__owner=request.user)
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()[:10]

    return render(request, 'search_results.html', {
        'query': query,
        'projects': projects,
        'tasks': tasks,
        'documents': documents,
        'total_results': len(projects) + len(tasks) + len(documents),
    })



