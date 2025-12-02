# -------------------------------------------------------------------
#                    VIEWS.UCETNICTVI_FDK_CZ.PY
# -------------------------------------------------------------------
# Zážitkové účetnictví pro subdoménu ucetnictvi.fdk.cz
# -------------------------------------------------------------------
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from fdk_cz.forms.accounting import (
    FreeInvoiceForm, InvoiceForm, InvoiceItemForm, InvoiceItemFormSet,
    AccountingContextForm, AccountingAccountForm, JournalEntryForm,
    JournalEntryLineFormSet, BalanceSheetForm
)
from fdk_cz.models import (
    Invoice, InvoiceItem,
    AccountingContext, AccountingAccount, JournalEntry, JournalEntryLine, BalanceSheet
)

# Import views that don't need subdomain customization
from fdk_cz.views.accounting import (
    create_invoice, free_invoice, detail_invoice, edit_invoice, delete_invoice,
    set_accounting_context, create_journal_entry, account_detail, create_account
)


# -------------------------------------------------------------------
#                    HELPER FUNCTIONS
# -------------------------------------------------------------------

def get_current_context(request):
    """Get the active accounting context for current user/session."""
    if not request.user.is_authenticated:
        return None

    # Try to get from session first
    context_id = request.session.get('accounting_context_id')
    if context_id:
        try:
            return AccountingContext.objects.get(context_id=context_id, user=request.user, is_active=True)
        except AccountingContext.DoesNotExist:
            pass

    # Fallback to most recent active context
    return AccountingContext.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-fiscal_year', 'name').first()


# -------------------------------------------------------------------
#                    DASHBOARD
# -------------------------------------------------------------------

def accounting_dashboard(request):
    """
    Hlavní dashboard pro zážitkové účetnictví.
    Pro nepřihlášené = DEMO mode s fake daty.
    Pro přihlášené = reálná data.
    """

    # ---------------------------------------------------------
    # SUBDOMÉNA + NEPŘIHLÁŠENÝ = DEMO ÚČETNICTVÍ
    # ---------------------------------------------------------
    if not request.user.is_authenticated:
        if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":

            demo_context = {
                "name": "eKultura – DEMO účetnictví",
                "organization": {"name": "eKultura, z.s."},
                "fiscal_year": 2025,
                "demo": True,
            }

            # DEMO DATA - Faktury
            demo_invoices = [
                {
                    "invoice_number": "2025-001",
                    "company": {"name": "Techno Web Solutions s.r.o."},
                    "total_amount": 45200,
                    "status": "paid",
                    "id": 1,
                },
                {
                    "invoice_number": "2025-002",
                    "company": {"name": "Malá Živnost – Jan Novák"},
                    "total_amount": 7890,
                    "status": "pending",
                    "id": 2,
                },
                {
                    "invoice_number": "2025-003",
                    "company": {"name": "Rychlé Služby s.r.o."},
                    "total_amount": 21500,
                    "status": "overdue",
                    "id": 3,
                },
                {
                    "invoice_number": "2025-004",
                    "company": {"name": "Digital Marketing Plus"},
                    "total_amount": 63000,
                    "status": "paid",
                    "id": 4,
                },
                {
                    "invoice_number": "2025-005",
                    "company": {"name": "Kavárna U Kocoura"},
                    "total_amount": 12400,
                    "status": "pending",
                    "id": 5,
                },
            ]

            # DEMO DATA - Journal Entries
            demo_journal = [
                {
                    "entry_date": datetime(2025, 11, 15),
                    "description": "Úhrada faktury 2025-001 – Techno Web",
                    "total_debit": 45200,
                    "total_credit": 45200,
                    "lines": [
                        {"account": {"account_number": "221", "name": "Bankovní účty"}},
                        {"account": {"account_number": "311", "name": "Odběratelé"}},
                    ]
                },
                {
                    "entry_date": datetime(2025, 11, 14),
                    "description": "Faktura za energie – PRE",
                    "total_debit": 8750,
                    "total_credit": 8750,
                    "lines": [
                        {"account": {"account_number": "502", "name": "Spotřeba energií"}},
                        {"account": {"account_number": "321", "name": "Dodavatelé"}},
                    ]
                },
                {
                    "entry_date": datetime(2025, 11, 12),
                    "description": "Výplata mezd zaměstnanci",
                    "total_debit": 125000,
                    "total_credit": 125000,
                    "lines": [
                        {"account": {"account_number": "521", "name": "Mzdové náklady"}},
                        {"account": {"account_number": "331", "name": "Zaměstnanci"}},
                    ]
                },
            ]

            context = {
                "current_context": demo_context,
                "accounting_contexts": [demo_context],

                "total_revenues": 1850000,
                "total_expenses": 1230500,
                "profit": 619500,

                "invoices": demo_invoices,
                "recent_journal_entries": demo_journal,

                "demo_warning": True,
            }

            return render(
                request,
                "accounting/subdomain/accounting_dashboard.html",
                context
            )

        # Normální FDK dashboard pro anonymní
        context = {
            'invoices': [],
            'accounting_contexts': [],
            'total_revenues': 0,
            'total_expenses': 0,
            'profit': 0,
        }
        return render(request, 'accounting/accounting_dashboard.html', context)


    # ---------------------------------------------------------
    # PŘIHLÁŠENÝ UŽIVATEL = REAL DATA
    # ---------------------------------------------------------
    invoices = Invoice.objects.filter(company__users=request.user)[:10]

    accounting_contexts = AccountingContext.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-fiscal_year', 'name')

    current_context = get_current_context(request)
    total_revenues = Decimal(0)
    total_expenses = Decimal(0)
    recent_journal_entries = []

    if current_context:
        entries = JournalEntry.objects.filter(context=current_context).prefetch_related('lines__account')

        for entry in entries:
            for line in entry.lines.all():
                account_number = line.account.account_number
                if account_number.startswith('6'):
                    total_revenues += line.credit_amount - line.debit_amount
                elif account_number.startswith('5'):
                    total_expenses += line.debit_amount - line.credit_amount

        recent_entries = JournalEntry.objects.filter(
            context=current_context
        ).prefetch_related('lines__account').order_by('-entry_date', '-entry_id')[:10]

        for entry in recent_entries:
            total_debit = sum(line.debit_amount for line in entry.lines.all())
            total_credit = sum(line.credit_amount for line in entry.lines.all())
            entry.total_debit = total_debit
            entry.total_credit = total_credit
            recent_journal_entries.append(entry)

    profit = total_revenues - total_expenses

    context = {
        'invoices': invoices,
        'company': request.user.companies.first(),
        'accounting_contexts': accounting_contexts,
        'current_context': current_context,
        'total_revenues': total_revenues,
        'total_expenses': total_expenses,
        'profit': profit,
        'recent_journal_entries': recent_journal_entries,
    }

    # Použít subdomain šablonu pokud jsme na subdoméně
    template = "accounting/accounting_dashboard.html"
    if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":
        template = "accounting/subdomain/accounting_dashboard.html"

    return render(request, template, context)


# -------------------------------------------------------------------
#                    JOURNAL LEDGER (Účetní deník)
# -------------------------------------------------------------------

@login_required
def journal_ledger(request):
    """Display journal ledger with entries."""
    current_context = get_current_context(request)

    if not current_context:
        messages.warning(request, 'Nejprve vyberte účetní kontext.')
        return redirect('select_accounting_context')

    entries = JournalEntry.objects.filter(
        context=current_context
    ).prefetch_related('lines__account').order_by('-entry_date', '-entry_id')

    # Add totals to each entry
    for entry in entries:
        entry.total_debit = sum(line.debit_amount for line in entry.lines.all())
        entry.total_credit = sum(line.credit_amount for line in entry.lines.all())

    context = {
        'entries': entries,
        'current_context': current_context,
    }

    template = "accounting/journal_ledger.html"
    if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":
        template = "accounting/subdomain/journal_ledger.html"

    return render(request, template, context)


# -------------------------------------------------------------------
#                    CHART OF ACCOUNTS (Účtová osnova)
# -------------------------------------------------------------------

@login_required
def chart_of_accounts(request):
    """Display chart of accounts."""
    current_context = get_current_context(request)

    if not current_context:
        messages.warning(request, 'Nejprve vyberte účetní kontext.')
        return redirect('select_accounting_context')

    accounts = AccountingAccount.objects.filter(
        context=current_context,
        is_active=True
    ).order_by('account_number')

    context = {
        'accounts': accounts,
        'current_context': current_context,
    }

    template = "accounting/chart_of_accounts.html"
    if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":
        template = "accounting/subdomain/chart_of_accounts.html"

    return render(request, template, context)


# -------------------------------------------------------------------
#                    BALANCE SHEET (Rozvaha)
# -------------------------------------------------------------------

@login_required
def balance_sheet_view(request, balance_type='opening'):
    """Display balance sheet (opening or closing)."""
    current_context = get_current_context(request)

    if not current_context:
        messages.warning(request, 'Nejprve vyberte účetní kontext.')
        return redirect('select_accounting_context')

    balances = BalanceSheet.objects.filter(
        context=current_context,
        balance_type=balance_type
    ).select_related('account').order_by('account__account_number')

    total_debit = sum(b.debit_balance for b in balances)
    total_credit = sum(b.credit_balance for b in balances)

    context = {
        'balances': balances,
        'current_context': current_context,
        'balance_type': balance_type,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }

    template = "accounting/balance_sheet.html"
    if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":
        template = "accounting/subdomain/balance_sheet.html"

    return render(request, template, context)


# -------------------------------------------------------------------
#                    INVOICES (Faktury)
# -------------------------------------------------------------------

@login_required
def list_invoices(request):
    """List all invoices."""
    invoices = Invoice.objects.filter(
        company__users=request.user
    ).order_by('-invoice_date', '-invoice_number')

    context = {
        'invoices': invoices,
    }

    template = "accounting/list_invoices.html"
    if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":
        template = "accounting/subdomain/list_invoices.html"

    return render(request, template, context)


# -------------------------------------------------------------------
#                    CONTEXT SELECTION
# -------------------------------------------------------------------

@login_required
def select_accounting_context(request):
    """Select active accounting context."""
    contexts = AccountingContext.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-fiscal_year', 'name')

    if request.method == 'POST':
        context_id = request.POST.get('context_id')
        if context_id:
            try:
                selected_context = AccountingContext.objects.get(
                    context_id=context_id,
                    user=request.user,
                    is_active=True
                )
                request.session['accounting_context_id'] = context_id
                messages.success(request, f'Aktivní kontext: {selected_context.name}')
                return redirect('accounting_dashboard')
            except AccountingContext.DoesNotExist:
                messages.error(request, 'Kontext nenalezen.')

    context = {
        'contexts': contexts,
    }

    template = "accounting/select_context.html"
    if hasattr(request, 'subdomain') and request.subdomain == "ucetnictvi":
        template = "accounting/subdomain/select_context.html"

    return render(request, template, context)
