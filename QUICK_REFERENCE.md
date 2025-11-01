# FDK.cz - Quick Reference Guide

## Key Facts
- **Framework**: Django 5.1 (Python)
- **Database**: MySQL (fdk_db, 41 tables, 42 models)
- **UI**: Custom CSS + Material Icons (responsive, sidebar-based)
- **Language**: Czech (primary), with English/German/Spanish support
- **Status**: 11 modules fully implemented, 5 module stubs

---

## 11 FULLY IMPLEMENTED MODULES

### 1. **Project Management** (`/projekty/`)
- Create projects with categories, milestones, documents
- Manage team with role-based access (ProjectUser, ProjectRole)
- View: 524 lines of code | Models: 10+ models

### 2. **Task Management** (`/spravce-ukolu/`)
- Create/edit/delete tasks with priority, status, due dates
- Assign to team members, add comments/attachments
- Subtask support via parent FK
- View: Integrated with project.py

### 3. **Grants & Dotations** (`/dotace/`)
- Grant programs, calls, requirements, applications
- Document upload, budget tracking, approval workflow
- View: 338 lines | Models: 5 core models

### 4. **Legal Compliance & Law AI** (`/zakony/`, `/ai-asistent/`)
- Law database search, AI query system
- Legal document templates, contract templates
- View: 356 lines | Models: 3 models

### 5. **Test Management** (`/testy/`)
- Test types, test cases, results (Pass/Fail/Blocked)
- Bug/error tracking with status workflow
- View: 205 lines | Models: 4 models

### 6. **Accounting & Invoicing** (`/ucetnictvi/`)
- Auto-generated invoices (YYYY-MM-NNNN format)
- VAT calculation, payment tracking
- View: 169 lines | Models: 2 models

### 7. **Warehouse Management** (`/sklady/`)
- Multiple warehouses with item inventory
- IN/OUT transactions, stock tracking
- View: 68 lines | Models: 3 models

### 8. **Contract Management** (`/kontrakty/`)
- Basic CRUD + file upload
- View: 66 lines | Models: 1 model

### 9. **Contact & Address Book** (`/kontakty/`)
- Personal/shared contacts with multi-org association
- View: 131 lines | Models: 1 model

### 10. **Lists/Sequences** (`/seznamy/`)
- Custom lists with granular permissions
- View: 136 lines | Models: 3 models

### 11. **Articles, Blog & Help** (`/clanky/`, `/napoveda/`)
- Content management (Page, Help, Blog, Announcement)
- Publishing control, featured articles
- View: 68 lines | Models: 1 model

---

## 5 INCOMPLETE MODULES (STUBS ONLY)
These have placeholder views/URLs but **no working implementation**:

1. **B2B Management** (`/` - not routed) - 25 lines, 0 models
2. **HR Management** - 31 lines, 0 models
3. **Risk Management** - 25 lines, 0 models
4. **IT Management** - 31 lines, 0 models
5. **Asset Management** - 25 lines, 0 models

---

## KEY MODELS & RELATIONSHIPS

### User/Organization
```
User (Django auth.User)
├── Organization (N:M via OrganizationMembership)
├── Company (N:M)
└── OrganizationMembership (role: admin|member|viewer)
```

### Project Hierarchy
```
Project
├── ProjectTask (with parent for subtasks)
├── ProjectMilestone
├── ProjectCategory
├── ProjectUser (role-based access via ProjectRole)
├── ProjectComment
├── ProjectDocument
├── ProjectAttachment
└── ProjectRole/ProjectPermission (RBAC system)
```

### Grants Workflow
```
GrantProgram
└── GrantCall (type: dotace|grant|stipendium)
    ├── GrantRequirement
    └── GrantApplication (status: draft→submitted→approved)
        └── GrantApplicationDocument
```

---

## AUTHENTICATION & AUTHORIZATION

### Login Flow
- **URL**: `/prihlaseni/` (Czech) or `/login/` (English)
- **Model**: Django's `auth.User`
- **Session-based**: Standard Django sessions
- **Protection**: `@login_required` decorator on views

### Authorization
- **Project-based RBAC**: ProjectRole → ProjectPermission mapping
- **List permissions**: Per-user can_edit/can_add controls
- **Ownership**: Project owner has full control

### NO Subscription System
- All authenticated users have access to all features
- No pricing tiers or module limitations
- Subscription models exist but are commented out

---

## DATABASE SCHEMA QUICK REFERENCE

| Category | Count | Key Tables |
|----------|-------|-----------|
| Authentication | 5 | User, auth_group, auth_permission |
| Projects | 11 | Project, ProjectTask, ProjectUser, ProjectMilestone |
| Grants | 5 | GrantProgram, GrantCall, GrantApplication |
| Finance | 2 | Invoice, InvoiceItem |
| Testing | 4 | Test, TestResult, TestError, TestType |
| Warehouse | 3 | Warehouse, WarehouseItem, WarehouseTransaction |
| Management | 12+ | Contact, Contract, Article, Law, LawQuery |
| Django Admin | 4+ | ContentType, Session, LogEntry, Permission |
| **TOTAL** | **41** | See FDK_REPOSITORY_OVERVIEW.md for full list |

---

## URL PATTERNS BY MODULE

| Module | Base URL | Key Routes |
|--------|----------|-----------|
| Projects | `/projekty/` | nowy-projekt, detail, edit, delete, manage-users |
| Tasks | `/spravce-ukolu/` | task-mgmt dashboard |
| Grants | `/dotace/` | programy, zadosti, kalendar |
| Law | `/zakony/`, `/dotaz/` | law-list, ai-asistent |
| Tests | `/testy/` | typy, vysledky, chyby |
| Invoicing | `/ucetnictvi/` | faktury, dashboard |
| Warehouse | `/sklady/` | project-stores, transactions |
| Lists | `/seznamy/` | seznam, items |
| Contacts | `/kontakty/` | list, create, detail |
| Contracts | `/kontrakty/` | list, create, detail |
| Articles | `/clanky/`, `/napoveda/` | blog-index, help-index, detail |

---

## SETTINGS & CONFIGURATION

### Current Settings
```
DATABASE: MySQL (fdk_db)
AUTH: Django auth.User
DEBUG: True (⚠️ production security risk)
LANGUAGE: Czech (cs)
TIMEZONE: UTC
ALLOWED_HOSTS: fdk.cz, www.fdk.cz, localhost, 127.0.0.1
```

### Important Paths
- **Templates**: `/fdk_cz/templates/`
- **Static**: `/static/`
- **Migrations**: `/fdk_cz/migrations/` (33 total)
- **Locale**: `/locale/` (Czech translations)

---

## DEVELOPMENT ROADMAP

### Priority 1: Complete Stub Modules
- [ ] Implement HR Management (models + views)
- [ ] Implement Risk Management (models + views)
- [ ] Implement B2B Management (models + views)
- [ ] Implement IT Management (models + views + ITIL)
- [ ] Implement Asset Management (models + views)

### Priority 2: Security & Admin
- [ ] Configure Django admin.py
- [ ] Set DEBUG=False for production
- [ ] Implement proper API documentation
- [ ] Add input validation/sanitization

### Priority 3: Enhancements
- [ ] Add REST API layer
- [ ] Implement real-time updates (WebSockets)
- [ ] Add audit logging
- [ ] Create test suite
- [ ] Improve permissions system

---

## QUICK STATS

- **Total Lines of Code**: ~2,400 (views only)
- **Total Models**: 42
- **Total Views**: 100+
- **Total URLs**: 120+
- **Form Classes**: 11+
- **Template Files**: 60+
- **CSS Lines**: 1000+
- **Migrations**: 33

---

## WHERE TO START

### For Bug Fixes
1. Check `/fdk_cz/views/` for the relevant module
2. Review `/fdk_cz/models.py` for data structure
3. Check `/fdk_cz/templates/` for the UI

### For New Features
1. Design models (add to models.py)
2. Create migration: `python manage.py makemigrations`
3. Create forms in `/fdk_cz/forms/`
4. Create views in `/fdk_cz/views/<module>.py`
5. Add URLs to `/fdk_cz/urls.py`
6. Create templates in `/fdk_cz/templates/<module>/`

### For Module Implementation
See "Stub Modules" section above - use existing modules as templates

---

## COMMON COMMANDS

```bash
# Database
python manage.py migrate
python manage.py makemigrations
python manage.py sqlmigrate fdk_cz 0001

# Running
python manage.py runserver

# Shell
python manage.py shell

# Static files
python manage.py collectstatic

# Database dump
mysqldump -u fdk -p fdk_db > fdk_db.sql
```

---

## Key Files to Know

- `/config/settings_template.py` - Main configuration
- `/config/urls.py` - Root URL routing
- `/fdk_cz/urls.py` - Module URLs (120+ patterns)
- `/fdk_cz/models.py` - All 42 database models
- `/fdk_cz/views/` - All view logic by module
- `/fdk_cz/forms/` - All form definitions
- `/fdk_cz/templates/base.html` - Main layout template
- `/fdk_cz/templates/inc/style.css` - Unified styling

---

For complete details, see: **FDK_REPOSITORY_OVERVIEW.md**
