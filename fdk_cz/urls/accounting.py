# -------------------------------------------------------------------
# URLS.ACCOUNTING.PY
# -------------------------------------------------------------------
from django.urls import path
from django.shortcuts import redirect

# Import views from subdomain-aware module
from fdk_cz.views.ucetnictvi_fdk_cz import *
from fdk_cz.views.user import login as main_login, registration as main_registration, logout as main_logout


def redirect_to_main_login(request):
    return redirect("https://fdk.cz/prihlaseni/?next=https://ucetnictvi.fdk.cz/")


# přesměrování subdomény na centrální login
def redirect_to_main_login(request):
    return redirect("https://fdk.cz/prihlaseni/?next=https://ucetnictvi.fdk.cz/")


def redirect_to_main_registration(request):
    return redirect("https://fdk.cz/registrace/?next=https://ucetnictvi.fdk.cz/")


def redirect_to_main_logout(request):
    return redirect("https://fdk.cz/odhlaseni/?next=https://ucetnictvi.fdk.cz/")


urlpatterns = [
    path("prihlaseni/", redirect_to_main_login, name="accounting_login"),
    path("registrace/", redirect_to_main_registration, name="accounting_registration"),
    path("odhlaseni/", redirect_to_main_logout, name="accounting_logout"),

    path('', accounting_dashboard, name='accounting_dashboard'),
    path('faktury/', list_invoices, name='list_invoices'),
    path('faktura/nova/', create_invoice, name='create_invoice'),
    path('faktura/bez-registrace/', free_invoice, name='free_invoice'),
    path('faktura/<int:invoice_id>/', detail_invoice, name='detail_invoice'),
    path('faktura/<int:invoice_id>/edit/', edit_invoice, name='edit_invoice'),
    path('faktura/<int:invoice_id>/delete/', delete_invoice, name='delete_invoice'),

    path('kontext/', select_accounting_context, name='select_accounting_context'),
    path('kontext/<int:context_id>/aktivovat/', set_accounting_context, name='set_accounting_context'),

    path('denik/', journal_ledger, name='journal_ledger'),
    path('denik/novy/', create_journal_entry, name='create_journal_entry'),

    path('uctova-osnova/', chart_of_accounts, name='chart_of_accounts'),
    path('uctova-osnova/novy/', create_account, name='create_account'),
    path('uctova-osnova/<int:account_id>/', account_detail, name='account_detail'),

    path('rozvaha/<str:balance_type>/', balance_sheet_view, name='balance_sheet_view'),
]
