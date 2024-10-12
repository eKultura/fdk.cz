# VIEWS.ACCOUNTING.PY

from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from fdk_cz.forms.accounting import FreeInvoiceForm, InvoiceForm, InvoiceItemForm, InvoiceItemFormSet
from fdk_cz.models import invoice, invoice_item
from urllib.parse import urlencode




def accounting_dashboard(request):
    # Získání seznamu faktur pro přihlášeného uživatele
    invoices = invoice.objects.filter(company__users=request.user)

    context = {
        'invoices': invoices,
        'company': request.user.companies.first(),
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
    invoice = get_object_or_404(invoice, pk=invoice_id)
    return render(request, 'accounting/detail_invoice.html', {'invoice': invoice})


@login_required
def list_invoices(request):
    invoices = invoice.objects.filter(company__users=request.user)
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
    invoice_instance = get_object_or_404(invoice, pk=invoice_id)
    
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










