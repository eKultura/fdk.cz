# -------------------------------------------------------------------
#                    FDK_CZ.URLS.PY
# -------------------------------------------------------------------

from django.urls import path


from fdk_cz.views.accounting import (
    accounting_dashboard, create_invoice, edit_invoice, delete_invoice, detail_invoice, free_invoice, list_invoices,
    select_accounting_context, set_accounting_context, chart_of_accounts, create_account,
    journal_ledger, create_journal_entry, balance_sheet_view
)
from fdk_cz.views.articles import article_detail, article_add, article_edit, article_blog_index, article_help_index, article_page_index
from fdk_cz.views.contact import create_contact, delete_contact, detail_contact, edit_contact, list_contacts
from fdk_cz.views.contract import create_contract, edit_contract, detail_contract, list_contracts

from fdk_cz.views.flist import add_item, create_list, delete_item, edit_item, edit_list, index_list, detail_list

from fdk_cz.views.grants import (
    # Program views
    program_list, program_detail, program_create, program_edit,
    
    # Call views (výzvy)
    grant_list, grant_detail, grant_create, grant_edit, grant_delete, grant_calendar,
    
    # Application views
    application_create, application_detail, application_edit, application_delete, application_list
)

from fdk_cz.views.index import index, dashboard
from fdk_cz.views.law import ai_assistant, contract_templates, create_query, law_dashboard, law_detail, law_documents, law_list, query_detail
from fdk_cz.views.project import create_category, create_document, create_task, create_milestone, detail_category, edit_category, edit_document, edit_milestone, edit_project, edit_task, delete_category, delete_document, delete_milestone, delete_project, delete_task, detail_document, detail_project, detail_task, index_project, join_project, new_project, manage_project_users, project_log, remove_project_user, take_task, task_management, update_task_status

from fdk_cz.views.test import (
    create_test, create_test_error, create_test_result, create_test_type,
    delete_test_error, detail_test_error, detail_test, detail_test_type,
    edit_test, edit_test_error, edit_test_type,
    list_test_errors, get_test_types, list_tests, list_test_results, list_test_types,
    mark_error_fixed,
    # Test Scenarios
    list_test_scenarios, create_test_scenario, detail_test_scenario,
    edit_test_scenario, delete_test_scenario
)

from fdk_cz.views.user import login, logout, user_profile, registration, user_settings, toggle_module_visibility
from fdk_cz.views.help import help_index, help_detail, help_add, help_edit, help_delete
from fdk_cz.views.organization import organization_dashboard, create_organization, organization_detail, add_member, remove_member, set_current_organization

from fdk_cz.views.warehouse import (
    all_stores,
    project_stores,
    organization_stores,
    store_detail,
    store_transactions,
    create_transaction,
    transaction_detail,
    create_warehouse,
    create_warehouse_for_project,
    create_warehouse_for_organization,
    create_warehouse_item,
    edit_warehouse_item,
    delete_warehouse_item,
    bulk_delete_warehouse_items,
    item_detail,
    create_warehouse_category,
    list_warehouse_categories,
)

from fdk_cz.views import subscription

# Import B2B views
from fdk_cz.views.b2b import (
    b2b_dashboard, list_companies, create_company, detail_company, edit_company, delete_company,
    list_contracts as list_b2b_contracts, create_contract as create_b2b_contract,
    detail_contract as detail_b2b_contract, edit_contract as edit_b2b_contract,
    delete_contract as delete_b2b_contract,
    list_documents as list_b2b_documents, create_document as create_b2b_document,
    delete_document as delete_b2b_document
)

# Import HR views
from fdk_cz.views.hr import (
    hr_dashboard, list_employees, create_employee, detail_employee, edit_employee, delete_employee,
    list_departments, create_department, detail_department, edit_department, delete_department
)

# Import Risk views
from fdk_cz.views.risk import (
    risk_dashboard, list_risks, create_risk, detail_risk, edit_risk, delete_risk, risk_matrix
)

# Import IT views
from fdk_cz.views.it import (
    it_dashboard, list_assets as list_it_assets, create_asset as create_it_asset,
    detail_asset as detail_it_asset, edit_asset as edit_it_asset, delete_asset as delete_it_asset,
    list_incidents as list_it_incidents, create_incident as create_it_incident,
    detail_incident as detail_it_incident, edit_incident as edit_it_incident,
    delete_incident as delete_it_incident
)

# Import Asset views
from fdk_cz.views.asset import (
    asset_dashboard, list_assets, create_asset, detail_asset, edit_asset, delete_asset,
    list_categories as list_asset_categories, create_category as create_asset_category,
    edit_category as edit_asset_category, delete_category as delete_asset_category
)

# Import DMS views
from fdk_cz.views.dms import (
    dms_public, dms_dashboard, dms_create_document
)

# Import Module landing pages
from fdk_cz.views.modules import (
    project_management_landing, grants_landing, accounting_landing, law_ai_landing
)

urlpatterns = [

    path('', index, name='index'),
    path('dashboard', dashboard, name='dashboard'),

    # Subscription URLs
    path('predplatne/', subscription.subscription_dashboard, name='subscription_dashboard'),
    path('ceny/', subscription.subscription_pricing, name='subscription_pricing'),
    path('predplatne/modul/<int:module_id>/objednat/', subscription.subscribe_to_module, name='subscribe_to_module'),
    path('predplatne/<int:subscription_id>/zrusit/', subscription.cancel_subscription, name='cancel_subscription'),
    path('predplatne/<int:subscription_id>/obnovit/', subscription.renew_subscription, name='renew_subscription'),

    # Subscription Admin URLs
    path('spravce/moduly/', subscription.admin_modules, name='admin_modules'),
    path('spravce/modul/<int:module_id>/upravit/', subscription.admin_edit_module, name='admin_edit_module'),
    path('spravce/priradit-modul/', subscription.admin_assign_module, name='admin_assign_module'),
    path('spravce/predplatne/', subscription.admin_subscriptions, name='admin_subscriptions'),

    # Auth paths
    path('prihlaseni/', login, name='login_cs'),
    path('odhlaseni/', logout, name='logout_cs'),
    path('odhlaseni/', logout, name='logout'),  # Alias for backward compatibility
    path('registrace/', registration, name='registration_cs'),
    path('profil/', user_profile, name='user_profile'),
    path('profil/nastaveni/', user_settings, name='user_settings'),
    path('profil/nastaveni/modul/<int:module_id>/toggle/', toggle_module_visibility, name='toggle_module_visibility'),

    # Organization paths
    path('organizace/', organization_dashboard, name='organization_dashboard'),
    path('organizace/nova/', create_organization, name='create_organization'),
    path('organizace/<int:organization_id>/', organization_detail, name='organization_detail'),
    path('organizace/<int:organization_id>/pridat-clena/', add_member, name='add_organization_member'),
    path('organizace/<int:organization_id>/odebrat-clena/<int:user_id>/', remove_member, name='remove_organization_member'),
    path('kontext/organizace/<int:organization_id>/', set_current_organization, name='set_organization_context'),
    path('kontext/osobni/', set_current_organization, name='set_personal_context'),

    # EN
    path('login/', login, name='login_en'),
    path('logout/', logout, name='logout_en'),  
    path('registration/', registration, name='registration_en'),


    # 🎯 Hlavní přehled dotací (výzev)
    path('dotace/', grant_list, name='grant_list'),
    path('dotace/novy/', grant_create, name='grant_create'),
    path('dotace/<int:grant_id>/', grant_detail, name='grant_detail'),
    path('dotace/<int:grant_id>/edit/', grant_edit, name='grant_edit'),
    path('dotace/<int:grant_id>/smazat/', grant_delete, name='grant_delete'),
    path('dotace/kalendar/', grant_calendar, name='grant_calendar'),

    # 🗂 Programy
    path('dotace/programy/', program_list, name='program_list'),
    path('dotace/programy/novy/', program_create, name='program_create'),
    path('dotace/program/<int:program_id>/', program_detail, name='program_detail'),
    path('dotace/program/<int:program_id>/edit/', program_edit, name='program_edit'),

    # 📝 Žádosti
    path('dotace/zadosti/', application_list, name='application_list'),
    path('dotace/zadost/<int:application_id>/', application_detail, name='application_detail'),
    path('dotace/zadost/novy/<int:call_id>/', application_create, name='application_create'),
    path('dotace/zadost/<int:application_id>/edit/', application_edit, name='application_edit'),
    path('dotace/zadost/<int:application_id>/smazat/', application_delete, name='application_delete'),


	# PRAVO
    path('pravo-ai/', law_dashboard, name='pravo_ai'),
    path('dotaz/', create_query, name='law_query'),
    path('dotaz/<int:query_id>/', query_detail, name='law_query_detail'),
    path('zakony/', law_list, name='law_list'),
    path('zakon/<int:law_id>/', law_detail, name='law_detail'),
    path('smlouvy/', contract_templates, name='law_contracts'),
    path('dokumenty/', law_documents, name='law_documents'),
    path('ai-asistent/', ai_assistant, name='law_ai_assistant'),


    # Project
    path('projekty/', index_project, name='index_project_cs'),
    path('projekt/novy-projekt', new_project, name='new_project_cs'),

    path('project/new-project', new_project, name='new_project_en'),
    path('neues-projekt/', new_project, name='new_project_de'),
    path('nuevo-proyecto/', new_project, name='new_project_es'),

    path('projekt/<int:project_id>/', detail_project, name='detail_project'),
    path('projekt/<int:project_id>/log/', project_log, name='project_log'),
    path('projekt/<int:project_id>/edit/', edit_project, name='edit_project_cs'),

    path('projekt/<int:project_id>/novy-ukol/', create_task, name='create_task'),
    path('projekt/ukol/<int:task_id>/', detail_task, name='detail_task'),
    path('projekt/ukol/<int:task_id>/upravit/', edit_task, name='edit_task'),
    path('projekt/ukol/<int:task_id>/smazat/', delete_task, name='delete_task'),
    path('projekt/ukol/<int:task_id>/status/<str:status>/', update_task_status, name='update_task_status'),
    path('projekt/ukol/<int:task_id>/prevzit/', take_task, name='take_task'),


    path('projekt/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('projekt/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projekt/<int:project_id>/delete/', delete_project, name='delete_project'),

    # Projects - management of users and roles
    path('projekt/<int:project_id>/uzivatele/', manage_project_users, name='manage_project_users'),
    path('projekt/<int:project_id>/uzivatel/<int:user_id>/smazat/', remove_project_user, name='remove_project_user'),
    path('projekt/<int:project_id>/pridat-se/', join_project, name='join_project'),
    path('projekt/<int:project_id>/novy-milnik/', create_milestone, name='create_milestone'),
    path('projekt/<int:project_id>/milnik/edit/<int:milestone_id>/', edit_milestone, name='edit_milestone'),
    path('projekt/<int:project_id>/milnik/<int:milestone_id>/smazat/', delete_milestone, name='delete_milestone'),


    path('projekt/<int:project_id>/nova_kategorie/', create_category, name='create_category'),
    path('projekt/kategorie/<int:category_id>/', detail_category, name='detail_category'),
    path('projekt/kategorie/<int:category_id>/editovat/', edit_category, name='edit_category'),
    path('projekt/kategorie/<int:category_id>/smazat/', delete_category, name='delete_category'),

    path('spravce-ukolu/', task_management, name='task_management'),


    # Projects - documents
    path('projekt/<int:project_id>/vytvorit-dokument/', create_document, name='create_document'),
    path('dokument/<int:document_id>/editovat/', edit_document, name='edit_document'),
    path('dokument/<int:document_id>/smazat/', delete_document, name='delete_document'),
    path('dokument/<int:document_id>/', detail_document, name='detail_document'),


    # Kontrakty UPRAVIT
    path('projects/<int:project_id>/contracts/create/', create_contract, name='create_contract'),
    path('kontrakty/', list_contracts, name='list_contracts'), #projects/<int:project_id>/contracts/
    path('contracts/<int:contract_id>/edit/', edit_contract, name='edit_contract'),
    path('contracts/<int:contract_id>/', detail_contract, name='detail_contract'),



    # SKLAD
    path('sklady/', all_stores, name='all_stores'),
    path('sklady/novy/', create_warehouse, name='create_warehouse'),
    path('sklady/kategorie/', list_warehouse_categories, name='list_warehouse_categories'),
    path('sklady/kategorie/nova/', create_warehouse_category, name='create_warehouse_category'),
    path('projekty/<int:project_id>/sklad/', project_stores, name='project_stores'),
    path('projekty/<int:project_id>/sklad/novy/', create_warehouse_for_project, name='create_warehouse_for_project'),
    path('organizace/<int:organization_id>/sklad/', organization_stores, name='organization_stores'),
    path('organizace/<int:organization_id>/sklad/novy/', create_warehouse_for_organization, name='create_warehouse_for_organization'),
    path('sklad/<int:store_id>/', store_detail, name='store_detail'),
    path('sklad/<int:store_id>/polozka/nova/', create_warehouse_item, name='create_warehouse_item'),
    path('sklad/<int:store_id>/polozky/smazat/', bulk_delete_warehouse_items, name='bulk_delete_warehouse_items'),
    path('sklad/polozka/<int:item_id>/', item_detail, name='item_detail'),
    path('sklad/polozka/<int:item_id>/upravit/', edit_warehouse_item, name='edit_warehouse_item'),
    path('sklad/polozka/<int:item_id>/smazat/', delete_warehouse_item, name='delete_warehouse_item'),
    path('sklad/<int:store_id>/transakce/', store_transactions, name='store_transactions'),
    path('sklad/<int:store_id>/transakce/nova/', create_transaction, name='create_transaction'),
    path('transakce/<int:transaction_id>/', transaction_detail, name='transaction_detail'),



    # LIST - SEZNAM
    path('seznamy/', index_list, name='index_list'),
    path('seznamy/novy-seznam/', create_list, name='create_list'),
    path('seznam/<int:list_id>/edit/', edit_list, name='edit_list'),
    path('seznam/<int:list_id>/polozka/pridat/', add_item, name='add_item'),
    path('seznam/<int:list_id>', detail_list, name='detail_list'),
    path('seznam/polozka/<int:item_id>/upravit/', edit_item, name='edit_item'),
    path('seznam/polozka/<int:item_id>/smazat/', delete_item, name='delete_item'),




    # Kontakt - soukromé a projektové
    path('muj-ucet/kontakty/', list_contacts, name='my_contacts'),
    path('projekt/<int:project_id>/kontakty/', list_contacts, name='project_contacts'),
    path('kontakty/', list_contacts, name='project_contacts'),
    path('kontakt/novy/<int:project_id>/', create_contact, name='create_contact_project'),
    path('kontakt/novy/', create_contact, name='create_contact_account'),
    path('kontakt/<int:contact_id>/edit/', edit_contact, name='edit_contact'),
    path('kontakt/<int:contact_id>/delete/', delete_contact, name='delete_contact'),
    path('kontakt/<int:contact_id>/', detail_contact, name='detail_contact'),

    # Kontrakt - projektové
    path('projekt/<int:project_id>/kontrakty/', list_contracts, name='project_contracts'),
    path('projekt/<int:project_id>/kontrakt/novy/', create_contract, name='create_contract'),
    path('kontrakt/<int:contract_id>/edit/', edit_contract, name='edit_contract'),
    path('kontrakt/<int:contract_id>/', detail_contract, name='detail_contract'),



    # TEST MANAGEMENT
    # Test Types

    path('testy/get_test_types/<int:project_id>/', get_test_types, name='get_test_types'),

    path('testy/typy/', list_test_types, name='list_test_types'),
    path('testy/typy/novy/', create_test_type, name='create_test_type'),
    path('testy/typy/<int:test_type_id>/', detail_test_type, name='detail_test_type'),
    path('testy/typy/<int:test_type_id>/edit/', edit_test_type, name='edit_test_type'),

    # Tests
    path('testy/', list_tests, name='list_tests'),
    path('testy/novy-test/', create_test, name='create_test'),
    path('testy/<int:test_id>/', detail_test, name='detail_test'),
    path('testy/<int:test_id>/edit/', edit_test, name='edit_test'),

    # Test Results
    path('testy/vysledky/', list_test_results, name='list_test_result'),
    path('testy/vysledky/novy/', create_test_result, name='create_test_result'),

    # Test Errors
    path('testy/chyby/', list_test_errors, name='list_test_errors'),
    path('testy/chyby/novy/', create_test_error, name='create_test_error'),
    path('projekt/<int:project_id>/chyby/novy/', create_test_error, name='create_test_error_for_project'),
    path('testy/chyby/<int:test_error_id>/upravit/', edit_test_error, name='edit_test_error'),
    path('testy/chyba/<int:test_error_id>/', detail_test_error, name='detail_test_error'),
    path('testy/chyba/<int:test_error_id>/opraveno/', mark_error_fixed, name='mark_error_fixed'),
    path('testy/delete/<int:error_id>/', delete_test_error, name='delete_test_error'),

    # Test Scenarios
    path('testy/scenare/', list_test_scenarios, name='list_test_scenarios'),
    path('testy/scenare/novy/', create_test_scenario, name='create_test_scenario'),
    path('testy/scenare/<int:scenario_id>/', detail_test_scenario, name='detail_test_scenario'),
    path('testy/scenare/<int:scenario_id>/upravit/', edit_test_scenario, name='edit_test_scenario'),
    path('testy/scenare/<int:scenario_id>/smazat/', delete_test_scenario, name='delete_test_scenario'),

    # Invoice management
    path('ucetnictvi/', accounting_dashboard, name='accounting_dashboard'),

    path('ucetnictvi/faktury/', list_invoices, name='list_invoices'),
    path('ucetnictvi/faktura/nova/', create_invoice, name='create_invoice'),
    path('ucetnictvi/faktura/bez-registrace/', free_invoice, name='free_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/edit/', edit_invoice, name='edit_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/delete/', delete_invoice, name='delete_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/', detail_invoice, name='detail_invoice'),

    # Accounting expansion - double-entry bookkeeping
    path('ucetnictvi/kontext/', select_accounting_context, name='select_accounting_context'),
    path('ucetnictvi/kontext/<int:context_id>/aktivovat/', set_accounting_context, name='set_accounting_context'),
    path('ucetnictvi/uctova-osnova/', chart_of_accounts, name='chart_of_accounts'),
    path('ucetnictvi/uctova-osnova/novy/', create_account, name='create_account'),
    path('ucetnictvi/denik/', journal_ledger, name='journal_ledger'),
    path('ucetnictvi/denik/novy/', create_journal_entry, name='create_journal_entry'),
    path('ucetnictvi/rozvaha/<str:balance_type>/', balance_sheet_view, name='balance_sheet_view'),


    # ======================================================================
    # B2B MANAGEMENT
    # ======================================================================
    path('b2b/', b2b_dashboard, name='b2b_dashboard'),

    # B2B Companies
    path('b2b/firmy/', list_companies, name='list_b2b_companies'),
    path('b2b/firma/nova/', create_company, name='create_b2b_company'),
    path('b2b/firma/<int:company_id>/', detail_company, name='detail_b2b_company'),
    path('b2b/firma/<int:company_id>/upravit/', edit_company, name='edit_b2b_company'),
    path('b2b/firma/<int:company_id>/smazat/', delete_company, name='delete_b2b_company'),

    # B2B Contracts
    path('b2b/smlouvy/', list_b2b_contracts, name='list_b2b_contracts'),
    path('b2b/smlouva/nova/', create_b2b_contract, name='create_b2b_contract'),
    path('b2b/smlouva/<int:contract_id>/', detail_b2b_contract, name='detail_b2b_contract'),
    path('b2b/smlouva/<int:contract_id>/upravit/', edit_b2b_contract, name='edit_b2b_contract'),
    path('b2b/smlouva/<int:contract_id>/smazat/', delete_b2b_contract, name='delete_b2b_contract'),

    # B2B Documents
    path('b2b/dokumenty/', list_b2b_documents, name='list_b2b_documents'),
    path('b2b/dokument/novy/', create_b2b_document, name='create_b2b_document'),
    path('b2b/dokument/<int:document_id>/smazat/', delete_b2b_document, name='delete_b2b_document'),


    # ======================================================================
    # HR MANAGEMENT
    # ======================================================================
    path('hr/', hr_dashboard, name='hr_dashboard'),

    # Employees
    path('hr/zamestnanci/', list_employees, name='list_employees'),
    path('hr/zamestnanec/novy/', create_employee, name='create_employee'),
    path('hr/zamestnanec/<int:employee_id>/', detail_employee, name='detail_employee'),
    path('hr/zamestnanec/<int:employee_id>/upravit/', edit_employee, name='edit_employee'),
    path('hr/zamestnanec/<int:employee_id>/smazat/', delete_employee, name='delete_employee'),

    # Departments
    path('hr/oddeleni/', list_departments, name='list_departments'),
    path('hr/oddeleni/nove/', create_department, name='create_department'),
    path('hr/oddeleni/<int:department_id>/', detail_department, name='detail_department'),
    path('hr/oddeleni/<int:department_id>/upravit/', edit_department, name='edit_department'),
    path('hr/oddeleni/<int:department_id>/smazat/', delete_department, name='delete_department'),


    # ======================================================================
    # RISK MANAGEMENT
    # ======================================================================
    path('rizika/', risk_dashboard, name='risk_dashboard'),
    path('rizika/seznam/', list_risks, name='list_risks'),
    path('rizika/nove/', create_risk, name='create_risk'),
    path('rizika/<int:risk_id>/', detail_risk, name='detail_risk'),
    path('rizika/<int:risk_id>/upravit/', edit_risk, name='edit_risk'),
    path('rizika/<int:risk_id>/smazat/', delete_risk, name='delete_risk'),
    path('rizika/matice/', risk_matrix, name='risk_matrix'),


    # ======================================================================
    # IT MANAGEMENT
    # ======================================================================
    path('it/', it_dashboard, name='it_dashboard'),

    # IT Assets
    path('it/aktiva/', list_it_assets, name='list_it_assets'),
    path('it/aktivum/nove/', create_it_asset, name='create_it_asset'),
    path('it/aktivum/<int:asset_id>/', detail_it_asset, name='detail_it_asset'),
    path('it/aktivum/<int:asset_id>/upravit/', edit_it_asset, name='edit_it_asset'),
    path('it/aktivum/<int:asset_id>/smazat/', delete_it_asset, name='delete_it_asset'),

    # IT Incidents (ITIL)
    path('it/incidenty/', list_it_incidents, name='list_it_incidents'),
    path('it/incident/novy/', create_it_incident, name='create_it_incident'),
    path('it/incident/<int:incident_id>/', detail_it_incident, name='detail_it_incident'),
    path('it/incident/<int:incident_id>/upravit/', edit_it_incident, name='edit_it_incident'),
    path('it/incident/<int:incident_id>/smazat/', delete_it_incident, name='delete_it_incident'),


    # ======================================================================
    # ASSET MANAGEMENT
    # ======================================================================
    path('majetek/', asset_dashboard, name='asset_dashboard'),

    # Assets
    path('majetek/seznam/', list_assets, name='list_assets'),
    path('majetek/novy/', create_asset, name='create_asset'),
    path('majetek/<int:asset_id>/', detail_asset, name='detail_asset'),
    path('majetek/<int:asset_id>/upravit/', edit_asset, name='edit_asset'),
    path('majetek/<int:asset_id>/smazat/', delete_asset, name='delete_asset'),

    # Asset Categories
    path('majetek/kategorie/', list_asset_categories, name='list_asset_categories'),
    path('majetek/kategorie/nova/', create_asset_category, name='create_asset_category'),
    path('majetek/kategorie/<int:category_id>/upravit/', edit_asset_category, name='edit_asset_category'),
    path('majetek/kategorie/<int:category_id>/smazat/', delete_asset_category, name='delete_asset_category'),

    # DMS - Document Management System
    path('dms/', dms_public, name='dms_public'),
    path('dms/dashboard/', dms_dashboard, name='dms_dashboard'),
    path('dms/dokument/novy/', dms_create_document, name='dms_create_document'),

    # Help & Documentation System
    path('dokumentace/', help_index, name='help_index'),
    path('dokumentace/pridat/', help_add, name='help_add'),
    path('dokumentace/<slug:slug>/', help_detail, name='help_detail'),
    path('dokumentace/<slug:slug>/upravit/', help_edit, name='help_edit'),
    path('dokumentace/<slug:slug>/smazat/', help_delete, name='help_delete'),

    # Articles
    path('clanky/', article_blog_index, name='article_blog_index'),
    path('napoveda/', article_help_index, name='article_help_index'),
    path('stranky/', article_page_index, name='article_page_index'),

    path('clanek/pridat', article_add, name='article_add'),
    path('upravit/<slug:slug>', article_edit, name='article_edit'),

    # ======================================================================
    # MODULE LANDING PAGES (for anonymous users)
    # ======================================================================
    path('modul/sprava-projektu/', project_management_landing, name='module_project_management'),
    path('modul/granty-dotace/', grants_landing, name='module_grants'),
    path('modul/ucetnictvi/', accounting_landing, name='module_accounting'),
    path('modul/ai-pravnik/', law_ai_landing, name='module_law_ai'),

    path('<slug:slug>', article_detail, name='article_detail'),

]



