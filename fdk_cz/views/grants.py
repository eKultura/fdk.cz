# -------------------------------------------------------------------
#                    VIEWS.GRANTS.PY
# -------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from datetime import date
import calendar

from fdk_cz.models import (
    GrantProgram,
    GrantCall,
    GrantApplication,
    Project,
    Company,
)


# ===================================================================
#                    1. PROGRAMS (GrantProgram)
# ===================================================================

def program_list(request):
    """Seznam všech grantových programů"""
    programs = GrantProgram.objects.filter(is_active=True).order_by("name")
    return render(request, "grants/program_list.html", {"programs": programs})


def program_detail(request, program_id):
    """Detail programu a jeho výzev"""
    program = get_object_or_404(GrantProgram, pk=program_id)
    calls = program.calls.all().order_by("-published_at")
    return render(
        request, "grants/program_detail.html", {"program": program, "calls": calls}
    )


@login_required
def program_create(request):
    """Vytvoření nového programu - pouze pro superadminy"""
    # Kontrola oprávnění - pouze superadmin může vytvářet programy
    if not request.user.is_superuser:
        messages.error(request, "Nemáte oprávnění k vytvoření programu. Pouze superadmin může vytvářet nové programy.")
        return redirect("program_list")

    if request.method == "POST":
        name = request.POST.get("name")
        provider = request.POST.get("provider")
        description = request.POST.get("description")
        total_budget = request.POST.get("total_budget") or None

        if not name:
            messages.error(request, "Název programu je povinný.")
        else:
            program = GrantProgram.objects.create(
                name=name,
                provider=provider,
                description=description,
                total_budget=total_budget,
                is_active=True,
            )
            messages.success(request, f'Program "{program.name}" byl vytvořen.')
            return redirect("program_detail", program_id=program.program_id)

    return render(request, "grants/program_create.html")


@login_required
def program_edit(request, program_id):
    """Úprava programu - pouze pro superadminy"""
    # Kontrola oprávnění - pouze superadmin může upravovat programy
    if not request.user.is_superuser:
        messages.error(request, "Nemáte oprávnění k úpravě programu. Pouze superadmin může upravovat programy.")
        return redirect("program_detail", program_id=program_id)

    program = get_object_or_404(GrantProgram, pk=program_id)
    if request.method == "POST":
        program.name = request.POST.get("name", program.name)
        program.provider = request.POST.get("provider", program.provider)
        program.description = request.POST.get("description", program.description)
        program.total_budget = request.POST.get("total_budget") or program.total_budget
        program.save()
        messages.success(request, "Program byl upraven.")
        return redirect("program_detail", program_id=program.program_id)
    return render(request, "grants/program_edit.html", {"program": program})


# ===================================================================
#                    2. GRANTS (výzvy)
# ===================================================================

def grant_list(request):
    """Seznam všech výzev (dotací)"""
    grants = GrantCall.objects.filter(is_active=True).order_by("-published_at")

    provider_filter = request.GET.get("provider")
    type_filter = request.GET.get("type")
    search_query = request.GET.get("search")

    if provider_filter:
        grants = grants.filter(provider=provider_filter)
    if type_filter:
        grants = grants.filter(type=type_filter)
    if search_query:
        from django.db.models import Q
        grants = grants.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(keywords__icontains=search_query)
        )

    # Rozdělení dotací podle typu pro zobrazení v template
    active_dotace = grants.filter(type='dotace')
    active_granty = grants.filter(type='grant')
    active_grants_count = grants.count()

    context = {
        "grants": grants,
        "active_dotace": active_dotace,
        "active_granty": active_granty,
        "active_grants_count": active_grants_count,
        "providers": GrantCall.objects.values_list("provider", flat=True).distinct(),
        "types": GrantCall._meta.get_field("type").choices,
    }
    return render(request, "grants/grant_list.html", context)


def grant_detail(request, grant_id):
    """Detail výzvy / dotace"""
    grant = get_object_or_404(GrantCall, pk=grant_id)
    applications = grant.applications.all()

    related_grants = (
        GrantCall.objects.filter(program=grant.program, is_active=True)
        .exclude(call_id=grant.call_id)
        .order_by("end_date")[:5]
    )

    context = {
        "grant": grant,
        "applications": applications,
        "related_grants": related_grants,
        "today": timezone.now().date(),
        "can_apply": request.user.is_authenticated and grant.is_active,
    }
    return render(request, "grants/grant_detail.html", context)


@login_required
def grant_create(request, program_id=None):
    """Vytvoření nové výzvy / dotace - pouze pro superadminy"""
    # Kontrola oprávnění - pouze superadmin může vytvářet dotace
    if not request.user.is_superuser:
        messages.error(request, "Nemáte oprávnění k vytvoření dotace. Pouze superadmin může vytvářet nové dotace.")
        return redirect("grant_list")

    program = None
    if program_id:
        program = get_object_or_404(GrantProgram, pk=program_id)

    if request.method == "POST":
        title = request.POST.get("title")
        provider = request.POST.get("provider")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None
        budget = request.POST.get("budget") or None
        grant_number = request.POST.get("grant_number") or None
        grant_subnumber = request.POST.get("grant_subnumber") or None

        grant = GrantCall.objects.create(
            program=program,
            title=title,
            provider=provider,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            grant_number=grant_number,
            grant_subnumber=grant_subnumber,
            status="open",
            is_active=True,
        )
        messages.success(request, f'Dotace "{grant.title}" byla vytvořena.')
        return redirect("grant_detail", grant_id=grant.call_id)

    return render(request, "grants/grant_create.html", {"program": program})


@login_required
def grant_edit(request, grant_id):
    """Editace výzvy / dotace - pouze pro superadminy"""
    # Kontrola oprávnění - pouze superadmin může upravovat dotace
    if not request.user.is_superuser:
        messages.error(request, "Nemáte oprávnění k úpravě dotace. Pouze superadmin může upravovat dotace.")
        return redirect("grant_detail", grant_id=grant_id)

    grant = get_object_or_404(GrantCall, pk=grant_id)
    if request.method == "POST":
        grant.title = request.POST.get("title", grant.title)
        grant.provider = request.POST.get("provider", grant.provider)
        grant.description = request.POST.get("description", grant.description)
        grant.start_date = request.POST.get("start_date") or grant.start_date
        grant.end_date = request.POST.get("end_date") or grant.end_date
        grant.budget = request.POST.get("budget") or grant.budget
        grant.grant_number = request.POST.get("grant_number") or grant.grant_number
        grant.grant_subnumber = request.POST.get("grant_subnumber") or grant.grant_subnumber
        grant.status = request.POST.get("status", grant.status)
        grant.save()
        messages.success(request, "Dotace byla upravena.")
        return redirect("grant_detail", grant_id=grant.call_id)
    return render(request, "grants/grant_edit.html", {"grant": grant})


@login_required
def grant_delete(request, grant_id):
    """Smazání dotace - pouze pro superadminy"""
    # Kontrola oprávnění - pouze superadmin může mazat dotace
    if not request.user.is_superuser:
        messages.error(request, "Nemáte oprávnění ke smazání dotace. Pouze superadmin může mazat dotace.")
        return redirect("grant_detail", grant_id=grant_id)

    grant = get_object_or_404(GrantCall, pk=grant_id)
    if request.method == "POST":
        grant.delete()
        messages.success(request, "Dotace byla smazána.")
        return redirect("grant_list")
    return render(request, "grants/grant_delete.html", {"grant": grant})



# ===================================================================
#                    3. APPLICATIONS (GrantApplication)
# ===================================================================

@login_required
def application_create(request, call_id):
    """Vytvoření žádosti k výzvě"""
    call = get_object_or_404(GrantCall, pk=call_id)

    existing_app = GrantApplication.objects.filter(
        call=call, applicant=request.user
    ).first()
    if existing_app:
        messages.warning(request, "Na tuto výzvu jste již podali žádost.")
        return redirect("application_edit", application_id=existing_app.application_id)

    user_projects = Project.objects.filter(owner=request.user)
    user_companies = Company.objects.filter(users=request.user)

    if request.method == "POST":
        project_id = request.POST.get("project_id")
        company_id = request.POST.get("company_id")
        requested_amount = request.POST.get("requested_amount") or 0
        notes = request.POST.get("notes", "").strip()

        app = GrantApplication.objects.create(
            call=call,
            project_id=project_id,
            organization_id=company_id,
            applicant=request.user,
            submission_date=timezone.now(),
            requested_amount=requested_amount,
            notes=notes,
            status="submitted",
        )
        messages.success(request, "Žádost byla úspěšně odeslána.")
        return redirect("grant_detail", grant_id=call.call_id)

    context = {
        "grant": call,  # Template používá 'grant'
        "call": call,  # Pro zpětnou kompatibilitu
        "projects": user_projects,
        "companies": user_companies
    }
    return render(request, "grants/application_create.html", context)


@login_required
def application_detail(request, application_id):
    """Detail žádosti"""
    app = get_object_or_404(GrantApplication, pk=application_id, applicant=request.user)
    return render(request, "grants/application_detail.html", {"application": app})


@login_required
def application_edit(request, application_id):
    """Editace žádosti"""
    app = get_object_or_404(GrantApplication, pk=application_id, applicant=request.user)

    user_projects = Project.objects.filter(owner=request.user)
    user_companies = Company.objects.filter(users=request.user)

    if request.method == "POST":
        action = request.POST.get("action", "save")

        if app.status == "draft":
            app.project_id = request.POST.get("project_id") or app.project_id
            app.organization_id = request.POST.get("company_id") or app.organization_id

        app.requested_amount = request.POST.get("requested_amount") or app.requested_amount
        app.notes = request.POST.get("notes", "").strip()

        if action == "submit" and app.status == "draft":
            app.status = "submitted"
            app.submission_date = timezone.now()
            messages.success(request, "Žádost byla odeslána.")
        else:
            messages.success(request, "Žádost byla uložena.")

        app.save()
        return redirect("grant_detail", grant_id=app.call.call_id)

    context = {"application": app, "projects": user_projects, "companies": user_companies}
    return render(request, "grants/application_edit.html", context)


@login_required
def application_delete(request, application_id):
    """Smazání žádosti (pouze draft)"""
    app = get_object_or_404(GrantApplication, pk=application_id, applicant=request.user)

    if app.status != "draft":
        messages.error(request, "Lze mazat pouze koncepty žádostí.")
        return redirect("grant_detail", grant_id=app.call.call_id)

    if request.method == "POST":
        call_id = app.call.call_id
        app.delete()
        messages.success(request, "Koncept žádosti byl smazán.")
        return redirect("grant_detail", grant_id=call_id)

    return render(request, "grants/application_delete.html", {"application": app})


@login_required
def application_list(request):
    """Seznam žádostí uživatele"""
    applications = GrantApplication.objects.filter(applicant=request.user).order_by(
        "-created_at"
    )

    status_filter = request.GET.get("status")
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(
        request,
        "grant_application_list.html",
        {"applications": applications, "status_choices": GrantApplication._meta.get_field("status").choices},
    )


# ===================================================================
#                    4. CALENDAR
# ===================================================================

def grant_calendar(request):
    """Kalendář výzev"""
    year = int(request.GET.get("year", date.today().year))
    months = [calendar.month_abbr[m] for m in range(1, 13)]

    calls = GrantCall.objects.filter(
        Q(start_date__year=year) | Q(end_date__year=year), is_active=True
    ).order_by("start_date")

    enriched = []
    for call in calls:
        start_month = call.start_date.month if call.start_date else 1
        end_month = call.end_date.month if call.end_date else 12
        enriched.append(
            {
                "call_id": call.call_id,
                "title": call.title,
                "provider": call.provider,
                "type": call.type,
                "start_date": call.start_date,
                "end_date": call.end_date,
                "start_month": start_month,
                "end_month": end_month,
            }
        )

    return render(
        request,
        "grants/grant_calendar.html",
        {"calls": enriched, "months": months, "range": range(1, 13), "year": year},
    )
