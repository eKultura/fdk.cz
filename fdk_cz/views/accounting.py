# -------------------------------------------------------------------
#                    VIEWS.ACCOUNTING.PY
# -------------------------------------------------------------------
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from fdk_cz.forms.accounting import (
    FreeInvoiceForm, InvoiceForm, InvoiceItemForm, InvoiceItemFormSet,
    AccountingContextForm, AccountingAccountForm, JournalEntryForm, JournalEntryLineFormSet, BalanceSheetForm
)
from fdk_cz.models import (
    Invoice, InvoiceItem,
    AccountingContext, AccountingAccount, JournalEntry, JournalEntryLine, BalanceSheet
)
from urllib.parse import urlencode

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------

def accounting_dashboard(request):
    if not request.user.is_authenticated:
        context = {
            'invoices': [],
            'company': None,
            'accounting_contexts': [],
            'total_revenues': 0,
            'total_expenses': 0,
            'profit': 0,
        }
        return render(request, 'accounting/accounting_dashboard.html', context)

    invoices = Invoice.objects.filter(company__users=request.user)[:10]  # Last 10 invoices

    # Get current organization context
    current_org_id = request.session.get('current_organization_id')

    # Get user's accounting contexts filtered by organization context
    if current_org_id:
        accounting_contexts = AccountingContext.objects.filter(
            user=request.user,
            is_active=True,
            organization_id=current_org_id
        ).order_by('-fiscal_year', 'name')
    else:
        accounting_contexts = AccountingContext.objects.filter(
            user=request.user,
            is_active=True,
            organization__isnull=True
        ).order_by('-fiscal_year', 'name')

    # Calculate income statement (výsledovka) for current context
    current_context = get_current_context(request)
    total_revenues = Decimal(0)
    total_expenses = Decimal(0)
    recent_journal_entries = []

    if current_context:
        # Get all journal entries for current context
        entries = JournalEntry.objects.filter(context=current_context).prefetch_related('lines__account')

        for entry in entries:
            for line in entry.lines.all():
                account_number = line.account.account_number
                # Revenue accounts (6xx in Czech accounting)
                if account_number.startswith('6'):
                    total_revenues += line.credit_amount - line.debit_amount
                # Expense accounts (5xx in Czech accounting)
                elif account_number.startswith('5'):
                    total_expenses += line.debit_amount - line.credit_amount

        # Get last 10 journal entries for current context
        recent_entries = JournalEntry.objects.filter(
            context=current_context
        ).prefetch_related('lines__account').order_by('-entry_date', '-entry_id')[:10]

        # Add total debit/credit to each entry
        recent_journal_entries = []
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
    return render(request, 'accounting/accounting_dashboard.html', context)




@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST, user=request.user)
        items_formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and items_formset.is_valid():
            invoice = form.save(commit=False)
            invoice.company = request.user.companies.first()  # Přiřazení první firmy uživatele
            invoice.save()
            items_formset.instance = invoice
            items_formset.save()
            return redirect('invoice_detail', invoice_id=invoice.invoice_id)
    else:
        form = InvoiceForm(user=request.user)
        items_formset = InvoiceItemFormSet()

    return render(request, 'accounting/create_invoice.html', {'form': form, 'items_formset': items_formset})



def detail_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'accounting/detail_invoice.html', {'invoice': invoice})


@login_required
def list_invoices(request):
    invoices = Invoice.objects.filter(company__users=request.user)
    return render(request, 'accounting/list_invoices.html', {'invoices': invoices})


@login_required
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        items_formset = InvoiceItemFormSet(request.POST, instance=invoice)
        if form.is_valid() and items_formset.is_valid():
            form.save()
            items_formset.save()
            return redirect('detail_invoice', invoice_id=invoice.invoice_id)
    else:
        form = InvoiceForm(instance=invoice)
        items_formset = InvoiceItemFormSet(instance=invoice)

    return render(request, 'accounting/edit_invoice.html', {'form': form, 'items_formset': items_formset, 'invoice': invoice})


@login_required
def delete_invoice(request, invoice_id):
    invoice_instance = get_object_or_404(Invoice, pk=invoice_id)
    
    if request.method == 'POST':
        invoice_instance.delete()
        return redirect('list_invoices') 

    return render(request, 'accounting/delete_invoice.html', {'invoice': invoice_instance})






def free_invoice(request):
    current_date = datetime.today().strftime('%Y-%m-%d')
    due_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')

    form = FreeInvoiceForm(request.GET or None)
    item_formset = InvoiceItemFormSet(request.GET or None)

    if form.is_valid() and item_formset.is_valid():
        data = form.cleaned_data
        items = item_formset.cleaned_data

        # Výpočet celkových cen a DPH
        vat_rate = Decimal(0) if data['without_vat'] else Decimal(data['vat_rate'])
        total_price = sum([Decimal(item['quantity']) * Decimal(item['unit_price']) for item in items if item.get('quantity') and item.get('unit_price')])
        vat_amount = total_price * (vat_rate / 100)
        total_with_vat = total_price + vat_amount

        # Generování čísla faktury
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        invoice_number = f"{current_year}-{current_month:02d}-{current_day}-01"

        # Předání formuláře a dalších dat do šablony
        context = {
            'form': form,
            'item_formset': item_formset,
            'items': items,
            'total_price': total_price,
            'vat_amount': vat_amount,
            'total_with_vat': total_with_vat,
            'invoice_number': invoice_number,
            'today': current_date,
            'due_date': due_date,
            'account_number': data.get('account_number', ''),  # Číslo účtu
            'bank_code': data.get('bank_code', ''),  # Kód banky
            # Údaje o dodavateli
            'company_name': data.get('company_name', ''),
            'street': data.get('street', ''),
            'street_number': data.get('street_number', ''),
            'city': data.get('city', ''),
            'postal_code': data.get('postal_code', ''),
            'ico': data.get('ico', ''),
            'dic': data.get('dic', ''),
            # Údaje o odběrateli
            'client_name': data.get('client_name', ''),
            'client_street': data.get('client_street', ''),
            'client_street_number': data.get('client_street_number', ''),
            'client_city': data.get('client_city', ''),
            'client_postal_code': data.get('client_postal_code', ''),
            'client_ico': data.get('client_ico', ''),
            'client_dic': data.get('client_dic', ''),
        }
        return render(request, 'accounting/free_invoice_output.html', context)
    
    # Pokud není formulář validní, vrátíme stránku s chybami a formulářem
    else:
        return render(request, 'accounting/free_invoice.html', {'form': form, 'item_formset': item_formset, 'today': current_date, 'due_date': due_date})


# -------------------------------------------------------------------
#                    ACCOUNTING EXPANSION VIEWS
# -------------------------------------------------------------------

@login_required
def select_accounting_context(request):
    """View for selecting or creating accounting context"""
    # Get user's contexts
    contexts = AccountingContext.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-fiscal_year', 'name')

    if request.method == 'POST':
        form = AccountingContextForm(request.POST, user=request.user)
        if form.is_valid():
            context = form.save(commit=False)
            context.user = request.user
            context.save()
            # Store selected context in session
            request.session['accounting_context_id'] = context.context_id
            return redirect('accounting_dashboard')
    else:
        form = AccountingContextForm(user=request.user)

    return render(request, 'accounting/select_context.html', {
        'form': form,
        'contexts': contexts
    })


@login_required
def set_accounting_context(request, context_id):
    """Set active accounting context in session"""
    context = get_object_or_404(AccountingContext, context_id=context_id, user=request.user)
    request.session['accounting_context_id'] = context_id
    return redirect('accounting_dashboard')


def get_current_context(request):
    """Helper to get current accounting context from session"""
    context_id = request.session.get('accounting_context_id')

    # Get current organization context
    current_org_id = request.session.get('current_organization_id')

    if context_id:
        try:
            context = AccountingContext.objects.get(context_id=context_id, user=request.user)
            # Verify context matches current organization context
            if current_org_id:
                if context.organization_id == current_org_id:
                    return context
            else:
                if context.organization is None:
                    return context
        except AccountingContext.DoesNotExist:
            pass

    # Return first active context matching organization context
    if current_org_id:
        return AccountingContext.objects.filter(
            user=request.user,
            is_active=True,
            organization_id=current_org_id
        ).first()
    else:
        return AccountingContext.objects.filter(
            user=request.user,
            is_active=True,
            organization__isnull=True
        ).first()


@login_required
def chart_of_accounts(request):
    """View chart of accounts"""
    context = get_current_context(request)
    if not context:
        return redirect('select_accounting_context')

    accounts = AccountingAccount.objects.filter(
        context=context,
        is_active=True
    ).order_by('account_number')

    return render(request, 'accounting/chart_of_accounts.html', {
        'context': context,
        'accounts': accounts
    })


@login_required
def create_account(request):
    """Create new account in chart of accounts"""
    from django.contrib import messages
    from django.db import IntegrityError

    context = get_current_context(request)
    if not context:
        return redirect('select_accounting_context')

    if request.method == 'POST':
        form = AccountingAccountForm(request.POST, context=context)
        if form.is_valid():
            try:
                account = form.save(commit=False)
                account.context = context
                account.save()
                messages.success(request, f'Účet "{account.account_number} - {account.name}" byl úspěšně vytvořen.')
                return redirect('chart_of_accounts')
            except IntegrityError:
                messages.error(request, f'Účet s číslem "{account.account_number}" již v tomto kontextu existuje. Zvolte prosím jiné číslo účtu.')
    else:
        form = AccountingAccountForm(context=context)

    return render(request, 'accounting/create_account.html', {
        'form': form,
        'context': context
    })


@login_required
def account_detail(request, account_id):
    """View account details"""
    context = get_current_context(request)
    if not context:
        return redirect('select_accounting_context')

    account = get_object_or_404(
        AccountingAccount,
        account_id=account_id,
        context=context
    )

    # Get journal entry lines for this account
    journal_lines = JournalEntryLine.objects.filter(
        account=account
    ).select_related('journal_entry').order_by('-journal_entry__entry_date')

    # Calculate account balance
    total_debit = sum(line.debit_amount for line in journal_lines)
    total_credit = sum(line.credit_amount for line in journal_lines)
    balance = total_debit - total_credit

    return render(request, 'accounting/account_detail.html', {
        'context': context,
        'account': account,
        'journal_lines': journal_lines,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'balance': balance
    })


@login_required
def journal_ledger(request):
    """View journal ledger (účetní deník)"""
    context = get_current_context(request)
    if not context:
        return redirect('select_accounting_context')

    entries = JournalEntry.objects.filter(
        context=context
    ).prefetch_related('lines__account').order_by('-entry_date', '-entry_number')

    # Calculate totals for each entry
    for entry in entries:
        entry.total_debit = sum(line.debit_amount for line in entry.lines.all())
        entry.total_credit = sum(line.credit_amount for line in entry.lines.all())

    return render(request, 'accounting/journal_ledger.html', {
        'context': context,
        'entries': entries
    })


@login_required
def create_journal_entry(request):
    """Create new journal entry"""
    context = get_current_context(request)
    if not context:
        return redirect('select_accounting_context')

    if request.method == 'POST':
        form = JournalEntryForm(request.POST, context=context, user=request.user)
        # Pass context to formset forms via form_kwargs
        formset = JournalEntryLineFormSet(
            request.POST,
            form_kwargs={'context': context}
        )

        if form.is_valid() and formset.is_valid():
            # Check that debits equal credits
            total_debit = sum(f.cleaned_data.get('debit_amount', 0) for f in formset if f.cleaned_data and not f.cleaned_data.get('DELETE'))
            total_credit = sum(f.cleaned_data.get('credit_amount', 0) for f in formset if f.cleaned_data and not f.cleaned_data.get('DELETE'))

            if total_debit != total_credit:
                form.add_error(None, f'Součet MD ({total_debit}) se nerovná součtu D ({total_credit}). Podvojný zápis musí být vyrovnaný.')
            else:
                entry = form.save(commit=False)
                entry.context = context
                entry.created_by = request.user
                entry.save()

                # Save lines
                for line_form in formset:
                    if line_form.cleaned_data and not line_form.cleaned_data.get('DELETE'):
                        line = line_form.save(commit=False)
                        line.journal_entry = entry
                        line.save()

                return redirect('journal_ledger')
    else:
        form = JournalEntryForm(context=context, user=request.user)
        formset = JournalEntryLineFormSet(
            queryset=JournalEntryLine.objects.none(),
            form_kwargs={'context': context}
        )

    return render(request, 'accounting/create_journal_entry.html', {
        'form': form,
        'formset': formset,
        'context': context
    })


@login_required
def balance_sheet_view(request, balance_type='opening'):
    """View balance sheet (rozvaha)"""
    context = get_current_context(request)
    if not context:
        return redirect('select_accounting_context')

    balances = BalanceSheet.objects.filter(
        context=context,
        fiscal_year=context.fiscal_year,
        balance_type=balance_type
    ).select_related('account').order_by('account__account_number')

    # Calculate totals
    total_debit = sum(b.debit_balance for b in balances)
    total_credit = sum(b.credit_balance for b in balances)

    return render(request, 'accounting/balance_sheet.html', {
        'context': context,
        'balances': balances,
        'balance_type': balance_type,
        'total_debit': total_debit,
        'total_credit': total_credit
    })









