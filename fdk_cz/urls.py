### fdk_cz.urls.py

from django.urls import path


from fdk_cz.views.accounting import accounting_dashboard, create_invoice, edit_invoice, delete_invoice, detail_invoice, free_invoice, list_invoices

from fdk_cz.views.contact import create_contact, delete_contact, detail_contact, edit_contact, list_contacts
from fdk_cz.views.contract import create_contract, edit_contract, detail_contract, list_contracts

from fdk_cz.views.flist import add_item, create_list,  edit_list, index_list, detail_list
from fdk_cz.views.index import index, dashboard

from fdk_cz.views.project import create_category, create_task, create_milestone, edit_category, edit_project, edit_task, delete_category, delete_project, delete_task, detail_project, detail_task, index_project, new_project, manage_project_users, remove_project_user, update_task_status
from fdk_cz.views.test import  create_test, create_test_error, create_test_result, create_test_type, detail_test_error, edit_test, edit_test_error,  edit_test_type, list_test_errors, get_test_types, list_tests, list_test_results, list_test_types
from fdk_cz.views.user import login, logout, user_profile, registration, user_settings

urlpatterns = (

    path('', index, name='index'),
    path('dashboard', dashboard, name='dashboard'),

    # Auth paths
    path('prihlaseni/', login, name='login_cs'),
    path('odhlaseni/', logout, name='logout_cs'),
    path('registrace/', registration, name='registration_cs'),
    path('profil/', user_profile, name='user_profile'),   
    path('nastaveni/', user_settings, name='user_settings'),   
         
    # EN
    path('login/', login, name='login_en'),
    path('logout/', logout, name='logout_en'),  
    path('registration/', registration, name='registration_en'),


    # Project
    path('projekty/', index_project, name='index_project_cs'),
    path('projekt/novy-projekt', new_project, name='new_project_cs'),

    path('project/new-project', new_project, name='new_project_en'),
    path('neues-projekt/', new_project, name='new_project_de'),
    path('nuevo-proyecto/', new_project, name='new_project_es'),
    # Další cesty pro různé jazyky


    path('projekt/<int:project_id>/', detail_project, name='detail_project'),
    path('projekt/<int:project_id>/edit/', edit_project, name='edit_project_cs'),

    path('projekt/<int:project_id>/novy-ukol/', create_task, name='create_task'),
    path('projekt/ukol/<int:task_id>/upravit/', edit_task, name='edit_task'),
    path('projekt/ukol/<int:task_id>/smazat/', delete_task, name='delete_task'),
    path('projekt/ukol/<int:task_id>/status/<str:status>/', update_task_status, name='update_task_status'),


    path('projekt/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('projekt/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projekt/<int:project_id>/delete/', delete_project, name='delete_project'),

    # Projects - management of users and roles
    path('projekty/<int:project_id>/users/', manage_project_users, name='manage_project_users'),
    path('projekty/<int:project_id>/users/<int:user_id>/remove/', remove_project_user, name='remove_project_user'),
    path('projekt/<int:project_id>/novy_milnik/', create_milestone, name='create_milestone'),

    path('projekt/<int:project_id>/nova_kategorie/', create_category, name='create_category'),
    path('projekt/kategorie/<int:category_id>/editovat/', edit_category, name='edit_category'),
    path('projekt/kategorie/<int:category_id>/smazat/', delete_category, name='delete_category'),


    # LIST - SEZNAM
    path('seznamy/', index_list, name='index_list'),
    path('seznamy/novy-seznam/', create_list, name='create_list'),
    path('seznam/<int:list_id>/edit/', edit_list, name='edit_list'),
    path('seznam/<int:list_id>/polozka/pridat/', add_item, name='add_item'),
    path('seznam/<int:list_id>', detail_list, name='detail_list'),
    

    
    
    # KONTAKTY
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

    # Invoice management
    path('ucetnictvi/', accounting_dashboard, name='accounting_dashboard'),

    path('ucetnictvi/faktury/', list_invoices, name='list_invoices'),
    path('ucetnictvi/faktura/nova/', create_invoice, name='create_invoice'),
    path('ucetnictvi/faktura/bez-registrace/', free_invoice, name='free_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/edit/', edit_invoice, name='edit_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/delete/', delete_invoice, name='delete_invoice'),
    path('ucetnictvi/faktura/<int:invoice_id>/', detail_invoice, name='detail_invoice'),




)



