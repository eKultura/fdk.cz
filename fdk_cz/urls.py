# -------------------------------------------------------------------
#                    FDK_CZ.URLS.PY
# -------------------------------------------------------------------

from django.urls import path


from fdk_cz.views.accounting import accounting_dashboard, create_invoice, edit_invoice, delete_invoice, detail_invoice, free_invoice, list_invoices
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
from fdk_cz.views.project import create_category, create_document, create_task, create_milestone, edit_category, edit_document, edit_milestone, edit_project, edit_task, delete_category, delete_document, delete_milestone, delete_project, delete_task, detail_document, detail_project, detail_task, index_project, new_project, manage_project_users, remove_project_user, task_management, update_task_status

from fdk_cz.views.test import  create_test, create_test_error, create_test_result, create_test_type, delete_test_error, detail_test_error, edit_test, edit_test_error,  edit_test_type, list_test_errors, get_test_types, list_tests, list_test_results, list_test_types

from fdk_cz.views.user import login, logout, user_profile, registration, user_settings

from fdk_cz.views.warehouse import (
    all_stores,
    project_stores,
    organization_stores,
    store_detail,
    store_transactions,
    create_transaction,
    transaction_detail,
)
urlpatterns = (

    path('', index, name='index'),
    path('dashboard', dashboard, name='dashboard'),

    # Auth paths
    path('prihlaseni/', login, name='login_cs'),
    path('odhlaseni/', logout, name='logout_cs'),
    path('registrace/', registration, name='registration_cs'),
    path('profil/', user_profile, name='user_profile'),   
    path('profil/nastaveni/', user_settings, name='user_settings'),   
         
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
    path('dotace/zadost/novy/<int:grant_id>/', application_create, name='application_create'),
    path('dotace/zadost/<int:application_id>/edit/', application_edit, name='application_edit'),
    path('dotace/zadost/<int:application_id>/smazat/', application_delete, name='application_delete'),


	# PRAVO
    path('', law_dashboard, name='pravo_ai'),
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
    path('projekt/<int:project_id>/edit/', edit_project, name='edit_project_cs'),

    path('projekt/<int:project_id>/novy-ukol/', create_task, name='create_task'),
    path('projekt/ukol/<int:task_id>/', detail_task, name='detail_task'),  
    path('projekt/ukol/<int:task_id>/upravit/', edit_task, name='edit_task'),
    path('projekt/ukol/<int:task_id>/smazat/', delete_task, name='delete_task'),
    path('projekt/ukol/<int:task_id>/status/<str:status>/', update_task_status, name='update_task_status'),


    path('projekt/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('projekt/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projekt/<int:project_id>/delete/', delete_project, name='delete_project'),

    # Projects - management of users and roles
    path('projekt/<int:project_id>/uzivatele/', manage_project_users, name='manage_project_users'),
    path('projekt/<int:project_id>/uzivatel/<int:user_id>/smazat/', remove_project_user, name='remove_project_user'),
    path('projekt/<int:project_id>/novy-milnik/', create_milestone, name='create_milestone'),
    path('projekt/<int:project_id>/milnik/edit/<int:milestone_id>/', edit_milestone, name='edit_milestone'),
    path('projekt/<int:project_id>/milnik/<int:milestone_id>/smazat/', delete_milestone, name='delete_milestone'),


    path('projekt/<int:project_id>/nova_kategorie/', create_category, name='create_category'),
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
    path('projekty/<int:project_id>/sklad/', project_stores, name='project_stores'),
    path('organizace/<int:organization_id>/sklad/', organization_stores, name='organization_stores'),
    path('sklad/<int:store_id>/', store_detail, name='store_detail'),
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
    path('testy/typy/<int:test_type_id>/edit/', edit_test_type, name='edit_test_type'),

    # Tests
    path('testy/', list_tests, name='list_tests'),
    path('testy/novy-test/', create_test, name='create_test'),
    path('testy/<int:test_id>/edit/', edit_test, name='edit_test'),

    # Test Results
    path('testy/vysledky/', list_test_results, name='list_test_result'),
    path('testy/vysledky/novy/', create_test_result, name='create_test_result'),

    # Test Errors
    path('testy/chyby/', list_test_errors, name='list_test_errors'),
    path('testy/chyby/novy/', create_test_error, name='create_test_error'),
    path('testy/chyby/<int:test_error_id>/upravit/', edit_test_error, name='edit_test_error'),
    path('testy/chyba/<int:test_error_id>/', detail_test_error, name='detail_test_error'),
    path('testy/delete/<int:error_id>/', delete_test_error, name='delete_test_error'),


    # Invoice management
    path('ucetnictvi/', accounting_dashboard, name='accounting_dashboard'),

    path('ucetnictvi/faktury/', list_invoices, name='list_invoices'),
    path('ucetnictvi/faktura/nova/', create_invoice, name='create_invoice'),
    path('ucetnictvi/faktura/bez-registrace/', free_invoice, name='free_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/edit/', edit_invoice, name='edit_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/delete/', delete_invoice, name='delete_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/', detail_invoice, name='detail_invoice'),

    # Articles
    path('clanky/', article_blog_index, name='article_blog_index'),
    path('napoveda/', article_help_index, name='article_help_index'),
    path('stranky/', article_page_index, name='article_page_index'),

    path('clanek/pridat', article_add, name='article_add'),
    path('upravit/<slug:slug>', article_edit, name='article_edit'),

    path('<slug:slug>', article_detail, name='article_detail'),

)



