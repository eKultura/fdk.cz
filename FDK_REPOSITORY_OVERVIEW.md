# FDK.cz Repository - Comprehensive Overview

## Executive Summary
FDK.cz is a **Django 5.1** web application for comprehensive organizational management. It's built in Czech (with multi-language support) and focuses on project management, grants administration, legal compliance, and various business operations. The application serves the eKultura organization (IČO: 21682305).

---

## 1. PROJECT STRUCTURE & ARCHITECTURE

### Directory Layout
```
/home/user/fdk.cz/
├── config/                          # Django configuration
│   ├── settings_template.py         # Main settings (MySQL, 41 tables)
│   ├── urls.py                      # Main URL routing
│   ├── wsgi.py                      # WSGI configuration
│   └── asgi.py                      # ASGI configuration
│
├── fdk_cz/                          # Main Django application
│   ├── models.py                    # 42 database models (see details below)
│   ├── views/                       # 11 view modules
│   │   ├── project.py               # Project & task management (524 lines)
│   │   ├── grants.py                # Grants/Dotations module (338 lines)
│   │   ├── law.py                   # Legal AI assistant (356 lines)
│   │   ├── test.py                  # Test management (205 lines)
│   │   ├── accounting.py            # Invoicing & accounting (169 lines)
│   │   ├── contact.py               # Contact management (131 lines)
│   │   ├── flist.py                 # Lists/Seznamy (136 lines)
│   │   ├── warehouse.py             # Warehouse management (68 lines)
│   │   ├── contract.py              # Contract management (66 lines)
│   │   ├── articles.py              # Blog/Help/Pages (68 lines)
│   │   ├── user.py                  # Auth/Registration (87 lines)
│   │   ├── index.py                 # Homepage/Dashboard (83 lines)
│   │   ├── hr.py                    # HR Management - STUB (31 lines)
│   │   ├── it.py                    # IT Management - STUB (31 lines)
│   │   ├── b2b.py                   # B2B Management - STUB (25 lines)
│   │   ├── risk.py                  # Risk Management - STUB (25 lines)
│   │   └── asset.py                 # Asset Management - STUB (25 lines)
│   │
│   ├── forms/                       # Form definitions
│   │   ├── project.py               # Project/task/milestone forms
│   │   ├── accounting.py            # Invoice forms
│   │   ├── contact.py               # Contact forms
│   │   ├── contract.py              # Contract forms
│   │   ├── warehouse.py             # Warehouse forms
│   │   ├── flist.py                 # List forms
│   │   ├── test.py                  # Test forms
│   │   ├── user.py                  # User/auth forms
│   │   ├── articles.py              # Article forms
│   │   └── index.py                 # Dashboard forms
│   │
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Main layout (Material Design)
│   │   ├── dashboard.html           # Dashboard
│   │   ├── project/                 # Project templates
│   │   ├── grants/                  # Grants templates
│   │   ├── law/                     # Legal assistant templates
│   │   ├── test/                    # Test management templates
│   │   ├── accounting/              # Invoice templates
│   │   ├── contact/                 # Contact templates
│   │   ├── list/                    # List templates
│   │   ├── warehouse/               # Warehouse templates
│   │   ├── contract/                # Contract templates
│   │   ├── articles/                # Article templates
│   │   ├── user/                    # Auth templates
│   │   ├── b2b/                     # B2B templates (STUB)
│   │   ├── inc/                     # Includes (CSS, helpers)
│   │   └── management/              # Management templates
│   │
│   ├── migrations/                  # 33 Django migrations
│   ├── admin.py                     # Django admin (not configured)
│   ├── apps.py                      # App config
│   └── urls.py                      # URL routing (comprehensive)
│
├── users/                           # Authentication app
│   ├── models.py                    # Uses Django's auth.User
│   ├── views.py                     # (empty - handled in fdk_cz)
│   ├── migrations/
│   └── admin.py
│
├── admin/                           # Admin static files
├── static/                          # Static assets
│   └── assets/scss/material-dashboard/   # Material Dashboard SCSS
├── locale/                          # i18n translations (Czech)
├── manage.py                        # Django management script
├── requirements.txt                 # Python dependencies
└── fdk_db.sql                       # Database dump (41 tables)
```

---

## 2. INSTALLED APPS & CONFIGURATION

### Django Setup
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'users',           # Custom users app
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fdk_cz',          # Main application
]
```

### Database
- **Engine**: MySQL (mysqlclient 2.2.4)
- **Name**: `fdk_db`
- **Tables**: 41 total
- **Key Field**: BigAutoField (Django 5.1 default)

### Authentication
- **Model**: Django's default `auth.User`
- **Login Required**: Most views have `@login_required`
- **URL**: `/prihlaseni/` (Czech), `/login/` (English)
- **Session-based**: Standard Django session middleware

### Multi-language Support
- **Languages**: Czech (primary), English, German, Spanish
- **Locale Path**: `/locale/`
- **Middleware**: `LocaleMiddleware` enabled
- **Default**: Czech (`LANGUAGE_CODE = 'cs'`)

---

## 3. DATABASE MODELS (42 MODELS)

### Core Organizational Models
```
Organization (model-based structure)
├── organization_id (PK)
├── name, ico
├── created_by (FK User)
├── members (M2M User via OrganizationMembership)
└── created_at

OrganizationMembership
├── user (FK)
├── organization (FK)
├── role (admin|member|viewer)
└── joined_at

User (Django auth.User)
├── Standard Django user fields
└── Related: projects, tasks, organizations, etc.

Company
├── company_id, name
├── Address fields (street, city, postal_code, state)
├── ico, dic (tax IDs)
├── is_vat_payer
├── users (M2M)
└── created_at
```

### Project Management Models
```
Project
├── project_id, name, description, url
├── start_date, end_date
├── owner (FK User)
├── public (boolean)
└── created

ProjectCategory
├── category_id, name
├── project (FK)
└── language

ProjectMilestone
├── milestone_id, title, description
├── due_date, status
├── created_at, updated_at

ProjectTask
├── task_id, title, description
├── category (FK ProjectCategory)
├── priority, status (Ke zpracování|Probíhá|Hotovo)
├── creator, assigned (FK User)
├── project (FK)
├── organization (FK Company)
├── due_date, created
├── parent (FK self - subtasks)

ProjectUser (Project-User assignment)
├── project_user_id
├── project, user (FK)
├── role (FK ProjectRole)
└── Unique: (project, user)

ProjectRole
├── role_id, role_name (unique)
└── Example: Administrator, Developer, Viewer

ProjectPermission
├── permission_id, permission_name (unique)

ProjectRolePermission
├── role (FK), permission (FK)
└── Unique: (role, permission)

ProjectAttachment
├── attachment_id, file_name, file_path
├── task (FK ProjectTask)
└── uploaded_by (FK User)

ProjectComment
├── comment_id, comment
├── task, user, project (FK)
└── posted

ProjectDocument
├── document_id, title
├── document_type, category (FK ProjectCategory)
├── file_path, url
├── project (FK), uploaded_by (FK User)
└── uploaded_at
```

### Grants & Dotations Module
```
GrantProgram
├── program_id, name
├── provider, description
├── total_budget
└── is_active

GrantCall (individual grant opportunities)
├── call_id, title
├── program (FK GrantProgram)
├── provider, description
├── type (dotace|grant|stipendium)
├── start_date, end_date, budget
├── eligibility, status (upcoming|open|closed)
├── is_active, published_at

GrantRequirement (per-call requirements)
├── requirement_id, name, description
├── call (FK GrantCall)
└── is_mandatory

GrantApplication
├── application_id
├── call (FK GrantCall)
├── project, organization (FK)
├── applicant (FK User)
├── submission_date, approval_date
├── requested_amount, granted_amount
├── status (draft|submitted|approved|rejected|in_progress)
├── is_successful, is_visible
├── notes, created_at, updated_at

GrantApplicationDocument
├── document_id
├── application (FK GrantApplication)
├── requirement (FK GrantRequirement - optional)
├── file, uploaded_at
```

### Test Management Module
```
TestType
├── test_type_id, name, description
├── project (FK)

Test
├── test_id, name, description
├── project (FK), test_type (FK)
├── grid_location (A1, B2, etc.)
└── date_created

TestResult
├── test_result_id
├── project, test (FK)
├── executed_by (FK User)
├── result (Pass|Fail|Blocked)
└── execution_date

TestError
├── test_error_id
├── test_result (FK)
├── project (FK)
├── error_title, description
├── steps_to_replicate
├── status (open|closed|in_progress)
├── created_by (FK User)
└── date_created
```

### Warehouse & Inventory
```
Warehouse
├── warehouse_id, name, location
└── created

WarehouseItem
├── item_id, name, description
├── quantity (PositiveInteger)
├── warehouse (FK)
└── created

WarehouseTransaction
├── transaction_id
├── item (FK WarehouseItem)
├── transaction_type (IN|OUT)
├── quantity, date
```

### Contracts & Documents
```
Contract
├── contract_id, name, description
├── start_date, end_date
├── project (FK)
└── document (FileField)
```

### Accounting & Invoicing
```
Invoice
├── invoice_id
├── company (FK Company)
├── invoice_number (auto-generated: YYYY-MM-NNNN)
├── issue_date, due_date
├── total_price, vat_amount, vat_rate (21% default)
├── is_paid
└── created_at

InvoiceItem
├── invoice_item_id
├── invoice (FK)
├── description, quantity, unit_price
├── total_price, vat_rate
```

### Lists & Collections
```
Flist (FDK List)
├── list_id, name, description
├── project (FK - optional)
├── owner (FK User)
├── is_private
├── created, modified

ListItem
├── item_id, content
├── flist (FK)
├── item_order, created, modified

ListPermission
├── list_permission_id
├── flist, user (FK)
├── can_edit, can_add
└── Unique: (flist, user)
```

### Contacts & Address Book
```
Contact
├── contact_id
├── first_name, last_name
├── phone, email
├── company (string)
├── description
├── project, organization, account (FK - optional)
├── is_private
├── added_on, last_contacted
```

### Legal Compliance
```
Law
├── id, title, number, year
├── content, category
├── effective_date
└── created_at

LawDocument
├── document_id, title
├── document_type, content
└── created_at

LawQuery
├── query_id, title, question
├── ai_response (optional)
├── status
└── created_at
```

### Content Management
```
Article
├── id, title, slug (unique)
├── category (Page|Help|Announcement|Blog|Internal)
├── content, summary
├── meta_header, meta_footer (for HTML injection)
├── author (FK User)
├── is_published, is_featured
├── created_at, updated_at
```

### Activity & Logging
```
ActivityLog
├── log_id
├── user (FK User)
├── user_action, description
└── date_time

Users2 (Legacy/Alternative)
├── user_id, username, email
├── password_hash, description
├── created, last_login
```

---

## 4. IMPLEMENTED MODULES (WITH FEATURES)

### 1. PROJECT MANAGEMENT ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Create, read, update, delete projects
- Project categories (Frontend, Backend, Database)
- Milestones with status tracking (planned|in_progress|completed)
- Task management (subtasks supported via parent FK)
- Project team management (add/remove users with roles)
- Documents per project
- Comments on tasks
- Task attachments
- Task status workflow (Ke zpracování → Probíhá → Hotovo)
- Task priority levels (Nice to have, etc.)
- Task assignment to users
- Dashboard with task statistics by status
- URL: `/projekty/`, `/projekt/<id>/`, `/projekt/<id>/novy-ukol/`

**Models**: Project, ProjectCategory, ProjectTask, ProjectMilestone, ProjectUser, ProjectRole, ProjectPermission, ProjectRolePermission, ProjectComment, ProjectDocument, ProjectAttachment

---

### 2. TASK MANAGEMENT ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Integrated within project management
- Task creation, editing, deletion
- Status updates (workflow: Nezahájeno → Probíhá → Hotovo)
- Assignment to team members
- Priority levels (Ke zpracování, Nice to have, etc.)
- Subtask support (parent field)
- Due date tracking
- Task categories per project
- Comments and collaboration
- Attachment support
- Organization-level tasks
- Central task management dashboard
- URL: `/spravce-ukolu/`, `/projekt/ukol/<id>/`

---

### 3. GRANTS & DOTATIONS ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Grant program management (create, edit, list)
- Individual grant call/opportunity listings
- Grant filtering (by provider, type: dotace|grant|stipendium)
- Grant calendars (deadline tracking)
- Application workflow (draft → submitted → approved|rejected)
- Multiple applications per grant call per user
- Document requirements per call
- Application document upload
- Budget tracking (requested vs. granted amount)
- Success tracking (is_successful flag)
- Visibility control (is_visible flag)
- Status management per application
- Related grants suggestions
- URL: `/dotace/`, `/dotace/programy/`, `/dotace/zadosti/`

**Models**: GrantProgram, GrantCall, GrantRequirement, GrantApplication, GrantApplicationDocument

---

### 4. LEGAL COMPLIANCE & LAW AI ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Law database (laws by number/year)
- Law search and detail views
- Legal document templates
- AI-powered legal query system
- Query response tracking
- Contract templates
- Legal documents library
- Dashboard with latest updates
- URL: `/zakony/`, `/zakon/<id>/`, `/dotaz/`, `/ai-asistent/`, `/smlouvy/`

**Models**: Law, LawDocument, LawQuery

---

### 5. TEST MANAGEMENT ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Test type management per project
- Individual test creation
- Test results tracking (Pass|Fail|Blocked)
- Test error/bug tracking
- Error status workflow (open → in_progress → closed)
- Steps to replicate documentation
- Test execution history
- Error detail pages
- Error deletion
- Project-specific test organization
- URL: `/testy/`, `/testy/typy/`, `/testy/vysledky/`, `/testy/chyby/`

**Models**: TestType, Test, TestResult, TestError

---

### 6. ACCOUNTING & INVOICING ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Invoice creation with auto-generated numbers (YYYY-MM-NNNN)
- Invoice items with VAT calculation (21% default rate configurable)
- Company association
- Invoice dates (issue and due)
- Payment status tracking
- Invoice templates (free invoice without registration)
- Invoice list, detail, edit, delete views
- Company VAT payer status
- Dashboard for accounting
- URL: `/ucetnictvi/`, `/ucetnictvi/faktury/`, `/ucetnictvi/faktura/nova/`

**Models**: Invoice, InvoiceItem, Company

---

### 7. WAREHOUSE MANAGEMENT ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Multiple warehouses (by organization/project)
- Item inventory tracking
- Transaction history (IN|OUT)
- Stock quantity management
- Warehouse detail views
- Transaction detail tracking
- New transaction creation
- Project-specific warehouses
- Organization-specific warehouses
- URL: `/sklady/`, `/sklad/<id>/`, `/sklad/<id>/transakce/`

**Models**: Warehouse, WarehouseItem, WarehouseTransaction

---

### 8. CONTRACT MANAGEMENT ✅ (PARTIALLY IMPLEMENTED)
**Status**: Basic implementation
- Contract creation, editing, deletion
- Contract listing
- Contract documents (file upload)
- Project association
- Contract dates (start/end)
- Contract descriptions
- Contract detail views
- URL: `/kontrakty/`, `/kontrakt/<id>/`

**Models**: Contract

---

### 9. CONTACT & ADDRESS BOOK ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Personal and shared contacts
- Contact creation, editing, deletion
- Contact association (project, organization, user account)
- Contact information (phone, email, company)
- Last contact tracking
- Contact detail views
- Private/shared toggle
- Company field (string-based CRM)
- URL: `/kontakty/`, `/kontakt/<id>/`

**Models**: Contact

---

### 10. LISTS/SEZNAM ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Create custom lists
- List items with ordering
- List sharing (permissions per user)
- Edit/delete items and lists
- Private/shared toggle
- Project association (optional)
- Owner management
- Permission control (can_edit, can_add)
- List detail pages
- URL: `/seznamy/`, `/seznam/<id>/`

**Models**: Flist, ListItem, ListPermission

---

### 11. ARTICLES, BLOG & HELP ✅ (WELL-IMPLEMENTED)
**Status**: Production-ready
- Article categories (Page, Help, Announcement, Blog, Internal)
- Article CRUD
- Slug-based URLs
- Publishing control
- Featured articles
- Author tracking
- Summary/excerpt support
- Meta tags support (header/footer HTML injection)
- Blog index, help index, pages index
- Article detail views
- URL: `/clanky/`, `/napoveda/`, `/stranky/`, `/<slug>/`

**Models**: Article

---

### 12. B2B MANAGEMENT ⚠️ (STUB - NOT IMPLEMENTED)
**Status**: Empty placeholder (25 lines)
- URLs defined but views return empty templates
- Intended for B2B client management
- No models defined
- Views: b2b_dashboard, b2b_clients, b2b_opportunities
- URL: Linked in sidebar but no functional templates

---

### 13. HR MANAGEMENT ⚠️ (STUB - NOT IMPLEMENTED)
**Status**: Empty placeholder (31 lines)
- URLs defined but views return empty templates
- Intended for employee management
- No models defined
- Views: hr_dashboard, hr_employees, hr_attendance, hr_leave
- URL: Linked in sidebar but no functional templates

---

### 14. RISK MANAGEMENT ⚠️ (STUB - NOT IMPLEMENTED)
**Status**: Empty placeholder (25 lines)
- URLs defined but views return empty templates
- Intended for risk tracking
- No models defined
- Views: risk_dashboard, risk_list, risk_matrix
- URL: Linked in sidebar but no functional templates

---

### 15. IT MANAGEMENT ⚠️ (STUB - NOT IMPLEMENTED)
**Status**: Empty placeholder (31 lines)
- URLs defined but views return empty templates
- Intended for IT asset/ticket management
- No models defined
- Views: it_dashboard, it_assets, it_tickets, it_licenses
- URL: Linked in sidebar but no functional templates

---

### 16. ASSET MANAGEMENT ⚠️ (STUB - NOT IMPLEMENTED)
**Status**: Empty placeholder (25 lines)
- URLs defined but views return empty templates
- Intended for asset/property tracking
- No models defined
- Views: asset_dashboard, asset_list, asset_maintenance
- URL: Linked in sidebar but no functional templates

---

### 17. DOCUMENT MANAGEMENT ✅ (PARTIALLY INTEGRATED)
**Status**: Partial - integrated into other modules
- Project documents
- Grant application documents
- Contract documents
- Test attachments
- No standalone DMS module
- Files stored in media folders

---

## 5. AUTHENTICATION & AUTHORIZATION

### Authentication System
```
LOGIN FLOW:
  User visits /prihlaseni/ or /login/
  → login view (user.py)
  → Django session authentication
  → Redirects to dashboard or next URL
  
REGISTRATION:
  User visits /registrace/ or /registration/
  → registration view
  → Creates new auth.User
  
LOGOUT:
  User clicks "Odhlásit se"
  → Clears session
  → Redirects to homepage
```

### Authorization Model
**Project-Based Roles & Permissions**:
```
ProjectRole (example roles defined):
  - Administrator
  - Developer
  - Viewer
  - (custom roles can be created)

ProjectPermission (example permissions):
  - Can view project
  - Can edit tasks
  - Can manage users
  - (flexible permission system)

ProjectRolePermission:
  Defines which permissions each role has
  Example: Admin role → all permissions
           Viewer role → read-only permissions

Access Control:
  - Project owner has full control
  - Team members have role-based access
  - @login_required decorator on views
```

**List-Based Permissions**:
```
ListPermission:
  - Granular per-user permissions on lists
  - can_edit: User can modify list items
  - can_add: User can add new items
```

### No Module/Subscription System Currently
- No pricing tiers
- No module subscriptions (commented out in models.py lines 690-722)
- No usage tracking (ModuleUsage model commented out)
- All authenticated users have access to all features

---

## 6. USER INTERFACE & TEMPLATES

### UI Framework
**Modern Minimalist Design**:
- Custom CSS (not Bootstrap/Material UI React)
- Material Icons for icons
- Inter font (Google Fonts)
- Responsive design
- Fixed sidebar navigation
- Fixed top header
- Single-column main content area

### Design System
**Color Scheme**:
- Primary Blue: #3b82f6
- Dark Text: #1e293b
- Light Background: #f8fafc
- Border Gray: #e2e8f0
- Sidebar Gray: #64748b

**Components**:
- `.header` - Fixed top navigation with search and user menu
- `.sidebar` - Fixed left sidebar with nav sections
- `.page-content` - Main content area
- `.nav-item`, `.nav-section` - Sidebar navigation
- `.form-control` - Standard form inputs
- `.btn` - Buttons (primary, outline styles)
- `.alert` - Message alerts
- `.breadcrumb` - Navigation breadcrumbs
- `.dropdown-menu` - User menu dropdown
- `.card` - Content cards (if used)
- `.table` - Data tables

### Menu Structure (sidebar.html / base.html)
```
HLAVNÍ (Main)
  ├─ Domů (Home)
  ├─ Dashboard
  └─ Právo AI (Legal AI)

MANAGEMENT
  ├─ Správa projektů (Project Management)
  ├─ Správa úkolů (Task Management)
  ├─ Správa B2B (B2B Management) - STUB
  ├─ HR Management - STUB
  ├─ Správa rizik (Risk Management) - STUB
  ├─ Správa IT (IT Management) - STUB
  └─ Správa majetku (Asset Management) - STUB

BUSINESS
  ├─ Smlouvy (Contracts)
  ├─ Granty & Dotace (Grants)
  ├─ Kontakty (Contacts)
  └─ Účetnictví (Accounting)

NÁSTROJE (Tools)
  ├─ Seznamy (Lists)
  ├─ Testování (Testing)
  └─ Sklad (Warehouse)
```

### Template Structure
```
base.html (main layout with sidebar + header)
├── dashboard.html
├── index.html
├── project/
│   ├── index_project.html
│   ├── new_project.html
│   ├── detail_project.html
│   ├── edit_project.html
│   ├── create_task.html
│   ├── detail_task.html
│   ├── edit_task.html
│   ├── delete_task.html
│   └── manage_project_users.html
├── grants/
│   ├── grant_list.html
│   ├── grant_detail.html
│   ├── grant_create.html
│   ├── grant_edit.html
│   ├── grant_delete.html
│   ├── grant_calendar.html
│   ├── application_create.html
│   ├── application_detail.html
│   ├── application_edit.html
│   └── application_delete.html
├── law/
│   ├── law_dashboard.html
│   ├── law_list.html
│   ├── law_detail.html
│   └── ai_assistant.html
├── test/
│   ├── list_tests.html
│   ├── create_test.html
│   ├── list_test_results.html
│   ├── list_test_errors.html
│   └── detail_test_error.html
├── accounting/
│   ├── accounting_dashboard.html
│   ├── list_invoices.html
│   ├── create_invoice.html
│   ├── invoice_detail.html
│   └── free_invoice.html
├── warehouse/
│   ├── all_stores.html
│   ├── store_detail.html
│   └── store_transactions.html
├── list/
│   ├── index_list.html
│   ├── create_list.html
│   ├── detail_list.html
│   └── edit_list.html
├── contact/
│   ├── list_contacts.html
│   ├── create_contact.html
│   ├── detail_contact.html
│   └── edit_contact.html
├── contract/
│   ├── list_contracts.html
│   ├── create_contract.html
│   └── detail_contract.html
├── articles/
│   ├── article_blog_index.html
│   ├── article_help_index.html
│   ├── article_page_index.html
│   ├── article_detail.html
│   └── article_form.html
├── user/
│   ├── login.html
│   ├── registration.html
│   ├── user_profile.html
│   └── user_settings.html
├── b2b/
│   ├── dashboard.html
│   ├── clients.html
│   └── opportunities.html
├── inc/
│   └── style.css (1000+ lines of unified CSS)
└── management/
    └── (various management views)
```

---

## 7. SETTINGS & CONFIGURATION

### Key Settings
```python
# Security
SECRET_KEY = 'django-insecure-[hidden]'
DEBUG = True  # ⚠️ Development mode
ALLOWED_HOSTS = ['www.fdk.cz', 'fdk.cz', 'localhost', '127.0.0.1', '194.182.77.136']
CSRF_COOKIE_SECURE = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fdk_db',
        'USER': 'fdk',
        'PASSWORD': 'very_strong_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Authentication
AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/prihlaseni/'

# Internationalization
LANGUAGE_CODE = 'cs'
LANGUAGES = [('cs', 'Czech'), ('en', 'English')]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Middleware
MIDDLEWARE = [
    'SecurityMiddleware',
    'SessionMiddleware',
    'CommonMiddleware',
    'CsrfViewMiddleware',
    'AuthenticationMiddleware',
    'MessageMiddleware',
    'ClickjackingMiddleware',
    'LocaleMiddleware',
]

# Apps
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### Dependencies
```
Django==5.1.1           # Main framework
mysqlclient==2.2.4      # MySQL driver
asgiref==3.8.1          # ASGI utilities
sqlparse==0.5.1         # SQL parsing
typing_extensions==4.12.2  # Type hints
uWSGI==2.0.26           # Production server
```

---

## 8. URL ROUTING OVERVIEW

### Complete URL Map
```
/prihlaseni/                                  → login (Czech)
/login/                                       → login (English)
/odhlaseni/                                   → logout (Czech)
/logout/                                      → logout (English)
/registrace/                                  → registration (Czech)
/registration/                                → registration (English)
/profil/                                      → user_profile
/profil/nastaveni/                            → user_settings

GRANTS & DOTATIONS:
/dotace/                                      → grant_list
/dotace/novy/                                 → grant_create
/dotace/<id>/                                 → grant_detail
/dotace/<id>/edit/                            → grant_edit
/dotace/<id>/smazat/                          → grant_delete
/dotace/kalendar/                             → grant_calendar
/dotace/programy/                             → program_list
/dotace/programy/novy/                        → program_create
/dotace/program/<id>/                         → program_detail
/dotace/program/<id>/edit/                    → program_edit
/dotace/zadosti/                              → application_list
/dotace/zadost/<id>/                          → application_detail
/dotace/zadost/novy/<grant_id>/               → application_create
/dotace/zadost/<id>/edit/                     → application_edit
/dotace/zadost/<id>/smazat/                   → application_delete

LAW & LEGAL:
/pravo_ai/                                    → law_dashboard
/dotaz/                                       → law_query (create)
/dotaz/<id>/                                  → law_query_detail
/zakony/                                      → law_list
/zakon/<id>/                                  → law_detail
/smlouvy/                                     → law_contracts (templates)
/dokumenty/                                   → law_documents
/ai-asistent/                                 → law_ai_assistant

PROJECTS:
/                                             → index (homepage)
/dashboard                                    → dashboard
/projekty/                                    → index_project
/projekt/novy-projekt                         → new_project
/projekt/<id>/                                → detail_project
/projekt/<id>/edit/                           → edit_project
/projekt/<id>/delete/                         → delete_project
/projekt/<id>/novy-ukol/                      → create_task
/projekt/ukol/<id>/                           → detail_task
/projekt/ukol/<id>/upravit/                   → edit_task
/projekt/ukol/<id>/smazat/                    → delete_task
/projekt/ukol/<id>/status/<status>/           → update_task_status
/projekt/<id>/uzivatele/                      → manage_project_users
/projekt/<id>/uzivatel/<user_id>/smazat/      → remove_project_user
/projekt/<id>/novy-milnik/                    → create_milestone
/projekt/<id>/milnik/edit/<milestone_id>/     → edit_milestone
/projekt/<id>/milnik/<milestone_id>/smazat/   → delete_milestone
/projekt/<id>/nova_kategorie/                 → create_category
/projekt/kategorie/<id>/editovat/             → edit_category
/projekt/kategorie/<id>/smazat/               → delete_category
/spravce-ukolu/                               → task_management

PROJECTS - Documents:
/projekt/<id>/vytvorit-dokument/              → create_document
/dokument/<id>/editovat/                      → edit_document
/dokument/<id>/smazat/                        → delete_document
/dokument/<id>/                               → detail_document

CONTRACTS:
/projects/<id>/contracts/create/              → create_contract
/kontrakty/                                   → list_contracts
/contracts/<id>/edit/                         → edit_contract
/contracts/<id>/                              → detail_contract
/projekt/<id>/kontrakty/                      → list_contracts (project-specific)
/projekt/<id>/kontrakt/novy/                  → create_contract

WAREHOUSE:
/sklady/                                      → all_stores
/projekty/<id>/sklad/                         → project_stores
/organizace/<id>/sklad/                       → organization_stores
/sklad/<id>/                                  → store_detail
/sklad/<id>/transakce/                        → store_transactions
/sklad/<id>/transakce/nova/                   → create_transaction
/transakce/<id>/                              → transaction_detail

LISTS:
/seznamy/                                     → index_list
/seznamy/novy-seznam/                         → create_list
/seznam/<id>/edit/                            → edit_list
/seznam/<id>/polozka/pridat/                  → add_item
/seznam/<id>/                                 → detail_list
/seznam/polozka/<id>/upravit/                 → edit_item
/seznam/polozka/<id>/smazat/                  → delete_item

CONTACTS:
/muj-ucet/kontakty/                           → list_contacts (personal)
/projekt/<id>/kontakty/                       → list_contacts (project-specific)
/kontakty/                                    → list_contacts (all)
/kontakt/novy/<id>/                           → create_contact (project)
/kontakt/novy/                                → create_contact (personal)
/kontakt/<id>/edit/                           → edit_contact
/kontakt/<id>/delete/                         → delete_contact
/kontakt/<id>/                                → detail_contact

TEST MANAGEMENT:
/testy/                                       → list_tests
/testy/novy-test/                             → create_test
/testy/<id>/edit/                             → edit_test
/testy/typy/                                  → list_test_types
/testy/typy/novy/                             → create_test_type
/testy/typy/<id>/edit/                        → edit_test_type
/testy/get_test_types/<project_id>/           → get_test_types (JSON endpoint)
/testy/vysledky/                              → list_test_results
/testy/vysledky/novy/                         → create_test_result
/testy/chyby/                                 → list_test_errors
/testy/chyby/novy/                            → create_test_error
/testy/chyby/<id>/upravit/                    → edit_test_error
/testy/chyba/<id>/                            → detail_test_error
/testy/delete/<id>/                           → delete_test_error

ACCOUNTING:
/ucetnictvi/                                  → accounting_dashboard
/ucetnictvi/faktury/                          → list_invoices
/ucetnictvi/faktura/nova/                     → create_invoice
/ucetnictvi/faktura/bez-registrace/           → free_invoice
/ucetnictvi/faktura/<id>/edit/                → edit_invoice
/ucetnictvi/faktura/<id>/delete/              → delete_invoice
/ucetnictvi/faktura/<id>/                     → detail_invoice

ARTICLES:
/clanky/                                      → article_blog_index
/napoveda/                                    → article_help_index
/stranky/                                     → article_page_index
/clanek/pridat                                → article_add
/upravit/<slug>/                              → article_edit
/<slug>/                                      → article_detail
```

---

## 9. KEY IMPLEMENTATION STATISTICS

| Metric | Count |
|--------|-------|
| Django Models | 42 |
| Database Tables | 41 |
| View Functions | 100+ |
| Form Classes | 11+ |
| Template Files | 60+ |
| URL Patterns | 120+ |
| Migrations | 33 |
| Fully Implemented Modules | 11 |
| Stub/Placeholder Modules | 5 |
| Total Python Files | 70+ |
| Lines of Code (views) | ~2,382 |
| CSS Lines | ~1,000+ |

---

## 10. CURRENT STATE & READY-FOR-PRODUCTION ASSESSMENT

### ✅ PRODUCTION-READY MODULES
1. Project Management
2. Task Management
3. Grants & Dotations
4. Test Management
5. Accounting & Invoicing
6. Warehouse Management
7. Contact Management
8. Lists/Sequences
9. Legal Compliance & Law AI
10. Articles/Blog/Help System

### ⚠️ PARTIALLY IMPLEMENTED
1. Contract Management (basic CRUD only)
2. Document Management (integrated, not standalone)

### ❌ NOT IMPLEMENTED (STUBS ONLY)
1. B2B Management
2. HR Management
3. Risk Management
4. IT Management
5. Asset Management

---

## 11. MIGRATION & DATABASE STATUS

### Latest Migration: #33
**0033_article.py** - Added Article model for blog/help/page content

### Migration History
- 0001_initial.py (195 lines) - Initial schema
- 0027_grantcall_grantprogram_law_and_more.py (319 lines) - Grant system
- 0030_law_detail_remove_lawquery_id_and_more.py (158 lines) - Law refinements

### Database Status
- MySQL `fdk_db` database exists with full schema
- fdk_db.sql (147KB) contains complete backup
- All 41 tables present
- Foreign key relationships established
- No data migration needed from legacy tables (Users2 exists but separate)

---

## 12. TECH STACK SUMMARY

**Framework**: Django 5.1 (Latest stable)
**Database**: MySQL 5.7+ (via mysqlclient)
**Python**: 3.8+
**Frontend**: HTML5 + Custom CSS (no React/Vue)
**Icons**: Material Icons
**Fonts**: Inter (Google Fonts)
**Server**: uWSGI (production deployment)
**Authentication**: Django's built-in session auth
**i18n**: Django's translation framework (Czech default)

---

## 13. KNOWN ISSUES & GAPS

1. **No admin.py configuration** - Django admin not configured
2. **DEBUG=True in production** - Security risk
3. **Module subscription system commented out** - No SaaS features
4. **No API layer** - Only HTML views, no REST API
5. **Limited error handling** - Some views lack validation
6. **No automated tests** - No test suite in repository
7. **Incomplete B2B/HR/Risk/IT/Asset modules** - Only view stubs
8. **Legacy Users2 table** - Duplicate user management
9. **No Docker/deployment config** - Manual server setup
10. **No async tasks** - No Celery/background jobs

---

## 14. RECOMMENDATIONS FOR DEVELOPMENT

### Priority 1 (Security/Critical)
- [ ] Set DEBUG=False in production
- [ ] Configure Django admin panel
- [ ] Add CORS/API security headers
- [ ] Implement rate limiting
- [ ] Add request validation on all forms

### Priority 2 (Feature Completion)
- [ ] Implement HR Management module (models + views)
- [ ] Implement Risk Management module (models + views)
- [ ] Implement B2B Management module (models + views)
- [ ] Implement IT Management module (models + views + ITIL practices)
- [ ] Implement Asset Management module (models + views)
- [ ] Add DMS (Document Management System) module

### Priority 3 (Enhancements)
- [ ] Add REST API layer (DRF)
- [ ] Implement WebSockets for real-time collaboration
- [ ] Add audit logging (activity tracking)
- [ ] Create test suite
- [ ] Add API documentation (Swagger)
- [ ] Implement async tasks (Celery)
- [ ] Add permissions middleware for fine-grained control

### Priority 4 (Optimization)
- [ ] Database indexing on frequently queried fields
- [ ] Caching layer (Redis)
- [ ] Pagination improvements
- [ ] Search functionality
- [ ] Export/import features
- [ ] Reporting/analytics dashboard

---

