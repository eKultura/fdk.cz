# CLAUDE.md - AI Assistant Guide for FDK.cz

> **Purpose**: This document provides comprehensive guidance for AI assistants working with the FDK.cz Django codebase. It explains architecture, conventions, workflows, and critical patterns to follow when developing features or fixing bugs.

**Last Updated**: 2025-12-04
**Django Version**: 5.1.1
**Database**: MySQL (fdk_db, 41 tables)
**Language**: Czech (primary), with multi-language support

---

## Table of Contents

1. [Codebase Overview](#codebase-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Development Workflows](#development-workflows)
4. [Critical Conventions](#critical-conventions)
5. [Module System & Subscriptions](#module-system--subscriptions)
6. [Organization Context System](#organization-context-system)
7. [Database Patterns](#database-patterns)
8. [Template & UI Conventions](#template--ui-conventions)
9. [Common Pitfalls](#common-pitfalls)
10. [Testing & Deployment](#testing--deployment)

---

## Codebase Overview

### Directory Structure

```
/home/user/fdk.cz/
├── config/                          # Django settings & configuration
│   ├── settings_template.py         # Main settings (DO NOT commit settings.py)
│   ├── urls.py                      # Root URL routing
│   ├── wsgi.py & asgi.py           # Server configurations
├── fdk_cz/                          # Main Django application
│   ├── models/                      # 21 modular model files
│   │   ├── __init__.py              # Imports all models
│   │   ├── user.py                  # User profiles, activity logs
│   │   ├── organization.py          # Organizations & memberships
│   │   ├── project.py               # Projects, tasks, SWOT
│   │   ├── modules.py               # Subscription system
│   │   ├── accounting.py            # Invoicing & double-entry
│   │   ├── grants.py                # Grant management
│   │   └── ... (15 more files)
│   ├── views/                       # 24 view modules (2400+ LOC total)
│   │   ├── project.py               # 1800+ lines
│   │   ├── grants.py                # 454 lines
│   │   └── ... (22 more files)
│   ├── forms/                       # 11+ form modules
│   ├── templates/                   # 26 template directories
│   ├── middleware/                  # Custom middleware
│   │   └── module_access.py         # Subscription enforcement
│   ├── context_processors.py        # Global context (menu, org context)
│   ├── utils/                       # Utilities (email, etc.)
│   └── management/commands/         # Management commands
├── users/                           # Authentication app (uses Django auth.User)
├── static/                          # Static assets (CSS, JS, images)
├── locale/                          # i18n translations (Czech primary)
└── Documentation files (9 MD files including this one)
```

### Tech Stack

- **Backend**: Django 5.1.1 (Python 3.8+)
- **Database**: MySQL via mysqlclient 2.2.4
- **Frontend**: Django templates + Custom CSS (no React/Vue)
- **Icons**: Material Icons (Google)
- **Server**: uWSGI 2.0.26 (production)
- **i18n**: Django translation framework (Czech default)

### Implemented Modules (11 Production-Ready)

1. ✅ **Project Management** (`/projekty/`) - Projects, tasks, milestones, SWOT, Gantt
2. ✅ **Task Management** (`/spravce-ukolu/`) - Central task dashboard
3. ✅ **Grants & Dotations** (`/dotace/`) - Grant programs, applications, documents
4. ✅ **Legal Compliance** (`/zakony/`) - Law database, AI assistant
5. ✅ **Test Management** (`/testy/`) - Test cases, results, bug tracking
6. ✅ **Accounting & Invoicing** (`/ucetnictvi/`) - Double-entry, invoices
7. ✅ **Warehouse Management** (`/sklady/`) - Inventory tracking
8. ✅ **Contract Management** (`/kontrakty/`) - Basic CRUD
9. ✅ **Contact Management** (`/kontakty/`) - Address book
10. ✅ **Lists** (`/seznamy/`) - Custom lists with permissions
11. ✅ **Articles/Blog/Help** (`/clanky/`) - Content management

### Stub Modules (Not Implemented)

⚠️ These have URLs but no functionality:
- B2B Management, HR Management, Risk Management, IT Management, Asset Management

---

## Architecture Patterns

### 1. Modular Model Structure

**CRITICAL**: Models are split into 21 separate files in `/fdk_cz/models/`. The `__init__.py` imports all models.

**Pattern**:
```python
# fdk_cz/models/module_name.py
from django.db import models
from django.contrib.auth.models import User

class ModelName(models.Model):
    # ALWAYS use explicit db_column
    model_id = models.AutoField(primary_key=True, db_column='model_id')

    # Foreign keys with related_name and db_column
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='model_items',
        db_column='user_id'
    )

    # ALWAYS specify db_table
    class Meta:
        db_table = 'FDK_model_name'  # FDK_ prefix is mandatory
```

### 2. Three-Tier Authorization System

The system has THREE levels of permissions:

#### Level 1: Organization Roles
```python
# models/organization.py
OrganizationRole (organization_owner, organization_admin, organization_member, organization_viewer)
├── OrganizationPermission (manage_members, view_data, etc.)
└── OrganizationRolePermission (mapping)

# Usage in views:
membership = OrganizationMembership.objects.filter(
    user=request.user,
    organization=org
).first()
if not membership or membership.role.role_name not in ['organization_owner', 'organization_admin']:
    return HttpResponseForbidden()
```

#### Level 2: Project Roles
```python
# models/project.py
ProjectRole (project_owner, project_admin, project_manager, project_editor, etc.)
├── ProjectPermission (view_project, edit_tasks, manage_users, etc.)
└── ProjectRolePermission (mapping)

# Usage in views:
project_user = ProjectUser.objects.filter(project=project, user=request.user).first()
if not project_user or not project_user.has_permission('edit_tasks'):
    return HttpResponseForbidden()
```

#### Level 3: Module Subscriptions
```python
# models/modules.py - SUBSCRIPTION SYSTEM
Module (catalog of available modules)
├── name (e.g., 'grants', 'accounting')
├── price_monthly, price_yearly
├── is_free (boolean)
└── url_patterns (JSONField for middleware)

UserModuleSubscription
├── user (FK)
├── module (FK)
├── organization (FK, optional - for org subscriptions)
├── subscription_type (free, monthly, yearly, lifetime, trial)
├── start_date, end_date
└── is_active

# Enforced by ModuleAccessMiddleware
```

### 3. Context Switching Architecture

**CRITICAL**: The application has a dual-context system for users working in personal vs organizational mode.

```python
# Context stored in session:
request.session['current_organization_id'] = org.organization_id

# Context available everywhere via context processor:
# fdk_cz/context_processors.py:organization_context()
{
    'current_organization': Organization instance or None,
    'is_personal_context': boolean,
    'user_organizations': queryset,
    'organization_role': membership.role if in org context
}

# Switching context:
def set_organization_context(request, organization_id):
    request.session['current_organization_id'] = organization_id
    return redirect('dashboard')

def set_personal_context(request):
    request.session.pop('current_organization_id', None)
    return redirect('dashboard')
```

**Usage Pattern in Views**:
```python
@login_required
def list_projects(request):
    current_org_id = request.session.get('current_organization_id')

    if current_org_id:
        # Organization context
        current_org = get_object_or_404(Organization, pk=current_org_id)
        projects = Project.objects.filter(organization=current_org)
    else:
        # Personal context
        projects = Project.objects.filter(
            owner=request.user,
            organization__isnull=True
        )

    return render(request, 'project/index_project.html', {
        'projects': projects
    })
```

### 4. View-Form-Template Pattern

**Standard Django pattern used throughout**:

```python
# File: fdk_cz/views/module.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def edit_item(request, item_id):
    # ALWAYS use get_object_or_404
    item = get_object_or_404(Model, pk=item_id)

    # Check permissions
    if item.owner != request.user:
        return HttpResponseForbidden('Nemáte oprávnění.')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Položka byla úspěšně upravena.')
            return redirect('detail_item', item_id=item.item_id)
    else:
        form = ItemForm(instance=item)

    return render(request, 'module/edit_item.html', {
        'form': form,
        'item': item
    })
```

---

## Development Workflows

### Adding a New Feature to Existing Module

**Example: Adding a "Priority" field to ProjectTask**

1. **Update Model** (`fdk_cz/models/project.py`):
   ```python
   class ProjectTask(models.Model):
       # ... existing fields ...
       priority = models.IntegerField(
           default=3,
           choices=[(1, 'Kritická'), (2, 'Vysoká'), (3, 'Normální'), (4, 'Nízká')],
           db_column='priority'
       )
   ```

2. **Create Migration**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Update Form** (`fdk_cz/forms/project.py`):
   ```python
   class task_form(forms.ModelForm):
       class Meta:
           model = ProjectTask
           fields = ['title', 'description', 'priority', ...]  # Add priority
           widgets = {
               'priority': forms.Select(attrs={'class': 'form-control'}),
           }
   ```

4. **Update Template** (`fdk_cz/templates/project/create_task.html`):
   ```django
   {{ form.priority.label_tag }}
   {{ form.priority }}
   ```

5. **Test**: Create/edit a task and verify priority is saved

### Creating a New Module from Scratch

**Example: Creating a "Documents" module**

1. **Create Model File** (`fdk_cz/models/documents.py`):
   ```python
   from django.db import models
   from django.contrib.auth.models import User

   class Document(models.Model):
       document_id = models.AutoField(primary_key=True, db_column='document_id')
       title = models.CharField(max_length=255, db_column='title')
       file = models.FileField(upload_to='documents/', db_column='file')
       uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploaded_by')
       created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

       class Meta:
           db_table = 'FDK_documents'
   ```

2. **Import in `models/__init__.py`**:
   ```python
   from .documents import *
   ```

3. **Create Migration**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Forms** (`fdk_cz/forms/documents.py`):
   ```python
   from django import forms
   from fdk_cz.models import Document

   class document_form(forms.ModelForm):
       class Meta:
           model = Document
           fields = ['title', 'file']
           widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control'}),
               'file': forms.FileInput(attrs={'class': 'form-control'}),
           }
   ```

5. **Create Views** (`fdk_cz/views/documents.py`):
   ```python
   from django.contrib.auth.decorators import login_required
   from django.shortcuts import render, redirect
   from fdk_cz.forms.documents import document_form

   @login_required
   def list_documents(request):
       documents = Document.objects.filter(uploaded_by=request.user)
       return render(request, 'documents/list.html', {'documents': documents})

   @login_required
   def create_document(request):
       if request.method == 'POST':
           form = document_form(request.POST, request.FILES)
           if form.is_valid():
               doc = form.save(commit=False)
               doc.uploaded_by = request.user
               doc.save()
               messages.success(request, 'Dokument byl úspěšně nahrán.')
               return redirect('list_documents')
       else:
           form = document_form()
       return render(request, 'documents/create.html', {'form': form})
   ```

6. **Add URLs** (`fdk_cz/urls/__init__.py`):
   ```python
   from fdk_cz.views import documents as documents_views

   urlpatterns = [
       # ... existing patterns ...
       path('dokumenty/', documents_views.list_documents, name='list_documents'),
       path('dokumenty/novy/', documents_views.create_document, name='create_document'),
   ]
   ```

7. **Create Templates** (`fdk_cz/templates/documents/list.html`):
   ```django
   {% extends 'base.html' %}
   {% block title %}Dokumenty{% endblock %}
   {% block content %}
   <h1>Dokumenty</h1>
   <a href="{% url 'create_document' %}" class="btn btn-primary">Nový dokument</a>
   <table class="table">
       {% for doc in documents %}
       <tr>
           <td>{{ doc.title }}</td>
           <td>{{ doc.created_at }}</td>
       </tr>
       {% endfor %}
   </table>
   {% endblock %}
   ```

8. **Add to Menu** (`fdk_cz/context_processors.py`):
   ```python
   MENU_CONFIG = {
       # ... existing config ...
       'modules': {
           'documents': {
               'name': 'Dokumenty',
               'icon': '&#128196;',
               'url': 'list_documents',
               'url_prefixes': ['documents', 'dokument'],
           }
       }
   }
   ```

9. **Register Module** (if subscription-gated):
   ```bash
   python manage.py shell
   >>> from fdk_cz.models import Module
   >>> Module.objects.create(
   ...     name='documents',
   ...     display_name='Dokumenty',
   ...     description='Správa dokumentů',
   ...     is_free=True,
   ...     url_patterns=['dokumenty/', 'dokument/']
   ... )
   ```

---

## Critical Conventions

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Database Tables | `FDK_` prefix, lowercase | `FDK_projects`, `FDK_tasks` |
| Primary Keys | `{model}_id` | `project_id`, `task_id` |
| Foreign Keys (db_column) | `{model}_id` | `user_id`, `project_id` |
| Model Classes | PascalCase | `Project`, `ProjectTask` |
| View Functions | lowercase_with_underscore | `detail_project`, `create_task` |
| Form Classes | lowercase_with_underscore | `project_form`, `task_form` |
| URL Names | Czech with underscores | `index_project_cs`, `create_task` |
| URL Paths | Czech | `/projekty/`, `/ukoly/`, `/dotace/` |
| Templates | lowercase_with_underscore | `detail_project.html` |

### Czech Language Usage

**CRITICAL**: All user-facing text, URLs, and variable names use Czech.

- **URL paths**: `/projekty/`, `/dotace/`, `/ucetnictvi/`
- **Messages**: `messages.success(request, 'Projekt byl úspěšně vytvořen.')`
- **Model verbose_name**: Use Czech in Meta class
- **Template text**: All Czech

### Database Column Naming

**ALWAYS use explicit `db_column` in models**:

```python
# ✅ CORRECT
user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')

# ❌ WRONG - Django will create user_id_id
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

### Form Widget Classes

**ALWAYS add Bootstrap-style classes**:

```python
class project_form(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
```

### Message Usage

**Use Django messages framework**:

```python
from django.contrib import messages

# Success
messages.success(request, 'Položka byla úspěšně vytvořena.')

# Error
messages.error(request, 'Chyba při ukládání dat.')

# Warning
messages.warning(request, 'Tato akce je nevratná.')

# Info
messages.info(request, 'Poznámka: Tato funkce je ve vývoji.')
```

---

## Module System & Subscriptions

### How the Module System Works

**Location**: `fdk_cz/models/modules.py`

```python
class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Internal name
    display_name = models.CharField(max_length=200)      # Shown in UI
    description = models.TextField()
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    url_patterns = models.JSONField(default=list)  # URLs this module covers
    is_active = models.BooleanField(default=True)
```

### Module Access Enforcement

**Middleware**: `fdk_cz/middleware/module_access.py`

This middleware runs on EVERY request and checks if the user has access to the requested URL.

**Logic**:
1. Check if URL matches any module's `url_patterns`
2. If yes, check if user has active `UserModuleSubscription` for that module
3. If no subscription, redirect to pricing page
4. Exempt URLs: authentication, static files, public pages

### Free vs Paid Modules

**Free modules** (always accessible):
- `project_management`
- `task_management`
- `lists`
- `contacts`

**Paid modules** (require subscription):
- `grants`
- `accounting`
- `warehouse`
- `law_ai`
- `hr_management`
- `risk_management`
- etc.

### User Module Preferences

Users can hide/show modules in their menu:

```python
class UserModulePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
```

### Checking Module Access in Views

```python
@login_required
def grants_dashboard(request):
    # Check if user has access to grants module
    has_access = UserModuleSubscription.objects.filter(
        user=request.user,
        module__name='grants',
        is_active=True
    ).exists()

    if not has_access:
        messages.error(request, 'Nemáte přístup k modulu Granty.')
        return redirect('pricing')

    # ... rest of view logic
```

---

## Organization Context System

### Understanding Context

**Two modes of operation**:

1. **Personal Context** - User works on their own data
   - `request.session['current_organization_id']` is None or missing
   - Projects filtered: `Project.objects.filter(owner=request.user, organization__isnull=True)`

2. **Organization Context** - User works within an organization
   - `request.session['current_organization_id']` = org.organization_id
   - Projects filtered: `Project.objects.filter(organization=current_org)`

### Context Processor

**Location**: `fdk_cz/context_processors.py:organization_context()`

Adds to EVERY template:
- `{{ current_organization }}` - Organization object or None
- `{{ is_personal_context }}` - Boolean
- `{{ user_organizations }}` - List of orgs user belongs to
- `{{ organization_role }}` - User's role in current org

### Context Switching Views

```python
# Set organization context
def set_organization_context(request, organization_id):
    org = get_object_or_404(Organization, pk=organization_id)

    # Verify membership
    if not OrganizationMembership.objects.filter(
        user=request.user,
        organization=org
    ).exists():
        return HttpResponseForbidden()

    request.session['current_organization_id'] = organization_id
    messages.success(request, f'Přepnuto do organizace: {org.name}')
    return redirect('dashboard')

# Set personal context
def set_personal_context(request):
    request.session.pop('current_organization_id', None)
    messages.success(request, 'Přepnuto do osobního režimu.')
    return redirect('dashboard')
```

### Visual Indicator

The sidebar shows current context:
- Personal mode: "Osobní režim" icon
- Organization mode: Organization name + icon

**Implementation** (`base.html`):
```django
<div class="context-indicator">
    {% if current_organization %}
        <span class="org-name">{{ current_organization.name }}</span>
        <a href="{% url 'set_personal_context' %}">Přepnout na osobní</a>
    {% else %}
        <span>Osobní režim</span>
        {% if user_organizations %}
            <select onchange="switchOrg(this.value)">
                <option>Přepnout na organizaci...</option>
                {% for org in user_organizations %}
                <option value="{{ org.organization_id }}">{{ org.name }}</option>
                {% endfor %}
            </select>
        {% endif %}
    {% endif %}
</div>
```

---

## Database Patterns

### Standard Model Structure

```python
class ModelName(models.Model):
    # 1. Primary key (explicit)
    model_id = models.AutoField(primary_key=True, db_column='model_id')

    # 2. User relationship (owner/creator)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_items',
        db_column='owner_id'
    )

    # 3. Organization relationship (for multi-tenancy)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='items',
        db_column='organization_id'
    )

    # 4. Core fields
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(blank=True, null=True, db_column='description')

    # 5. Status/state
    is_active = models.BooleanField(default=True, db_column='is_active')

    # 6. Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_model_name'  # REQUIRED
        ordering = ['-created_at']   # Optional but recommended
        indexes = [                  # Add for frequently queried fields
            models.Index(fields=['owner', 'is_active']),
        ]

    def __str__(self):
        return self.name
```

### Many-to-Many Relationships

**Use explicit through models** for flexibility:

```python
# ❌ AVOID simple M2M
class Project(models.Model):
    members = models.ManyToManyField(User)

# ✅ USE explicit through model
class ProjectUser(models.Model):
    project_user_id = models.AutoField(primary_key=True, db_column='project_user_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE, db_column='role_id')
    joined_at = models.DateTimeField(auto_now_add=True, db_column='joined_at')

    class Meta:
        db_table = 'FDK_project_users'
        unique_together = ['project', 'user']
```

### JSONField Usage

**For flexible data structures**:

```python
class SwotAnalysis(models.Model):
    data = models.JSONField(default=dict, db_column='data')
    # Stores: {
    #   'strengths': ['...', '...'],
    #   'weaknesses': ['...', '...'],
    #   'opportunities': ['...', '...'],
    #   'threats': ['...', '...']
    # }

class Module(models.Model):
    url_patterns = models.JSONField(default=list, db_column='url_patterns')
    # Stores: ['dotace/', 'dotace/program/', 'dotace/zadost/']
```

### Invoice Numbering Pattern

**Auto-generated invoice numbers**:

```python
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True, db_column='invoice_number')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Format: YYYY-MM-NNNN (e.g., 2025-12-0001)
            today = timezone.now()
            prefix = today.strftime('%Y-%m')
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=prefix
            ).order_by('-invoice_number').first()

            if last_invoice:
                last_num = int(last_invoice.invoice_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.invoice_number = f"{prefix}-{new_num:04d}"

        super().save(*args, **kwargs)
```

---

## Template & UI Conventions

### Template Inheritance

**Base template**: `fdk_cz/templates/base.html`

All templates extend base:

```django
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block breadcrumb %}
<nav class="breadcrumb">
    <a href="{% url 'dashboard' %}">Dashboard</a>
    <span>/</span>
    <a href="{% url 'index_project_cs' %}">Projekty</a>
    <span>/</span>
    <span>{{ project.name }}</span>
</nav>
{% endblock %}

{% block content %}
<div class="container">
    <h1>Page Heading</h1>
    <!-- Content here -->
</div>
{% endblock %}
```

### Menu System

**Dynamic menu** generated by `context_processors.py:user_modules()`

**Structure**:
- Menu defined in `MENU_CONFIG` dictionary
- Categories: Management, Finance, Business, Nástroje
- Each module has submenu items
- Active module detected by URL matching

**Example config**:
```python
MENU_CONFIG = {
    'categories': [
        {
            'name': 'Management',
            'icon': '&#128295;',
            'modules': ['project_management', 'task_management']
        }
    ],
    'modules': {
        'project_management': {
            'name': 'Správa projektů',
            'icon': '&#128295;',
            'url': 'index_project_cs',
            'url_prefixes': ['project', 'projekt'],
            'submenu': [
                {'name': 'Seznam projektů', 'url': 'index_project_cs', 'icon': '&#128203;'},
                {'name': 'Nový projekt', 'url': 'create_project_cs', 'icon': '&#10133;'},
            ]
        }
    }
}
```

### CSS Classes

**Standard classes** (defined in `static/css/fdkHome.css`):

- `.form-control` - Form inputs
- `.btn`, `.btn-primary`, `.btn-outline` - Buttons
- `.alert`, `.alert-success`, `.alert-error` - Messages
- `.breadcrumb` - Breadcrumb navigation
- `.sidebar`, `.nav-item`, `.nav-section` - Sidebar
- `.header` - Top header
- `.page-content` - Main content area
- `.table` - Data tables
- `.card` - Content cards

### Form Rendering

**Standard pattern**:

```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}

    {% if form.errors %}
    <div class="alert alert-error">
        <strong>Chyba:</strong> Opravte prosím chyby ve formuláři.
    </div>
    {% endif %}

    {% for field in form %}
    <div class="form-group">
        {{ field.label_tag }}
        {{ field }}
        {% if field.errors %}
        <span class="error">{{ field.errors.0 }}</span>
        {% endif %}
    </div>
    {% endfor %}

    <button type="submit" class="btn btn-primary">Uložit</button>
    <a href="{% url 'cancel_url' %}" class="btn btn-outline">Zrušit</a>
</form>
```

---

## Common Pitfalls

### 1. Forgetting db_column

**Problem**: Django auto-generates column names incorrectly for ForeignKeys.

```python
# ❌ WRONG - creates user_id_id in database
user = models.ForeignKey(User, on_delete=models.CASCADE)

# ✅ CORRECT
user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
```

### 2. Not Checking Organization Context

**Problem**: Views show data from all organizations.

```python
# ❌ WRONG
projects = Project.objects.filter(owner=request.user)

# ✅ CORRECT
current_org_id = request.session.get('current_organization_id')
if current_org_id:
    projects = Project.objects.filter(organization_id=current_org_id)
else:
    projects = Project.objects.filter(owner=request.user, organization__isnull=True)
```

### 3. Missing Permission Checks

**Problem**: Users can access/modify data they shouldn't.

```python
# ❌ WRONG
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect('index_project_cs')

# ✅ CORRECT
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Check ownership
    if project.owner != request.user:
        # Or check if user is in project team
        if not ProjectUser.objects.filter(project=project, user=request.user).exists():
            messages.error(request, 'Nemáte oprávnění smazat tento projekt.')
            return redirect('detail_project', project_id=project_id)

    project.delete()
    messages.success(request, 'Projekt byl smazán.')
    return redirect('index_project_cs')
```

### 4. Not Using get_object_or_404

**Problem**: 500 errors instead of 404.

```python
# ❌ WRONG
project = Project.objects.get(pk=project_id)  # Raises DoesNotExist

# ✅ CORRECT
project = get_object_or_404(Project, pk=project_id)  # Returns 404 page
```

### 5. Forgetting CSRF Token

**Problem**: POST requests fail with 403.

```django
<!-- ❌ WRONG -->
<form method="post">
    <!-- No CSRF token -->
</form>

<!-- ✅ CORRECT -->
<form method="post">
    {% csrf_token %}
    <!-- Form fields -->
</form>
```

### 6. Not Using Messages Framework

**Problem**: No user feedback after actions.

```python
# ❌ WRONG
def create_project(request):
    # ... create project ...
    return redirect('index_project_cs')  # Silent success

# ✅ CORRECT
def create_project(request):
    # ... create project ...
    messages.success(request, 'Projekt byl úspěšně vytvořen.')
    return redirect('index_project_cs')
```

### 7. Hardcoding URLs

**Problem**: URLs break when changed.

```python
# ❌ WRONG
return redirect('/projekty/')
<a href="/projekt/123/">Detail</a>

# ✅ CORRECT
return redirect('index_project_cs')
<a href="{% url 'detail_project' project.project_id %}">Detail</a>
```

### 8. Missing related_name

**Problem**: Reverse relationships are unclear.

```python
# ❌ WRONG
user = models.ForeignKey(User, on_delete=models.CASCADE)
# Access: user.projecttask_set.all() (unclear)

# ✅ CORRECT
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
# Access: user.tasks.all() (clear)
```

---

## Testing & Deployment

### Manual Testing Checklist

**No automated test suite exists yet.** When testing features:

1. **Authentication**:
   - [ ] Login/logout works
   - [ ] Registration creates user
   - [ ] @login_required redirects to login

2. **Permissions**:
   - [ ] Owners can edit/delete
   - [ ] Non-owners cannot edit/delete
   - [ ] Organization members see org data
   - [ ] Personal context shows only personal data

3. **Forms**:
   - [ ] All fields render correctly
   - [ ] Validation errors display
   - [ ] Success messages show
   - [ ] Data saves to database

4. **Context Switching**:
   - [ ] Can switch to organization
   - [ ] Can switch to personal mode
   - [ ] Data filters correctly in each context
   - [ ] Visual indicator shows current context

5. **Module Access**:
   - [ ] Free modules accessible to all
   - [ ] Paid modules block non-subscribers
   - [ ] Subscription grants access

### Database Migrations

**Always create migrations after model changes**:

```bash
# Create migration
python manage.py makemigrations

# Review migration file
cat fdk_cz/migrations/00XX_auto_YYYYMMDD_HHMM.py

# Apply migration
python manage.py migrate

# If needed, rollback
python manage.py migrate fdk_cz 00XX
```

### Management Commands

**Initialize system data**:

```bash
# Initialize roles and permissions
python manage.py init_roles

# Initialize module catalog
python manage.py init_modules
```

### Deployment Steps

1. **Update code**: `git pull origin main`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run migrations**: `python manage.py migrate`
4. **Collect static files**: `python manage.py collectstatic --no-input`
5. **Restart uWSGI**: `sudo systemctl restart uwsgi`
6. **Check logs**: `tail -f /var/log/uwsgi/fdk.log`

### Environment Variables

**CRITICAL**: Never commit `config/settings.py` or `.env` to git.

**.env file structure**:
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DB_NAME=fdk_db
DB_USER=fdk_user
DB_PASSWORD=strong-password
DB_HOST=localhost
DB_PORT=3306
ALLOWED_HOSTS=fdk.cz,www.fdk.cz
EMAIL_HOST=smtp.seznam.cz
EMAIL_PORT=465
EMAIL_HOST_USER=noreply@fdk.cz
EMAIL_HOST_PASSWORD=email-password
```

---

## Quick Reference Commands

### Django Management

```bash
# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Show migrations
python manage.py showmigrations

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

### Git Workflow

```bash
# Check status
git status

# Create feature branch
git checkout -b feature/new-feature

# Stage changes
git add .

# Commit
git commit -m "Add new feature"

# Push
git push origin feature/new-feature

# Merge to main
git checkout main
git merge feature/new-feature
git push origin main
```

### Database

```bash
# Dump database
mysqldump -u fdk_user -p fdk_db > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u fdk_user -p fdk_db < backup_20251204.sql

# Access MySQL
mysql -u fdk_user -p fdk_db
```

---

## Additional Resources

### Documentation Files

- **FDK_REPOSITORY_OVERVIEW.md** - Comprehensive technical overview
- **QUICK_REFERENCE.md** - Quick facts and stats
- **METODIKA.FDK.md** - Methodology documentation (Czech)
- **GRANTS_MODULE_ENHANCEMENT.md** - Grants module documentation
- **SUBSCRIPTION_SYSTEM_DESIGN.md** - Subscription system details
- **ROLES_PERMISSIONS_GUIDE.md** - Authorization system guide
- **DEPLOYMENT_INSTRUCTIONS.md** - Deployment procedures

### Key Files to Reference

| Purpose | File Path |
|---------|-----------|
| Settings template | `/config/settings_template.py` |
| Root URLs | `/config/urls.py` |
| App URLs | `/fdk_cz/urls/__init__.py` |
| All models | `/fdk_cz/models/__init__.py` |
| Context processors | `/fdk_cz/context_processors.py` |
| Module middleware | `/fdk_cz/middleware/module_access.py` |
| Base template | `/fdk_cz/templates/base.html` |
| Main CSS | `/static/css/fdkHome.css` |

### Model Files

| Domain | File Path |
|--------|-----------|
| Users & profiles | `/fdk_cz/models/user.py` |
| Organizations | `/fdk_cz/models/organization.py` |
| Projects & tasks | `/fdk_cz/models/project.py` |
| Subscriptions | `/fdk_cz/models/modules.py` |
| Grants | `/fdk_cz/models/grants.py` |
| Accounting | `/fdk_cz/models/accounting.py` |
| Legal | `/fdk_cz/models/law.py` |
| Testing | `/fdk_cz/models/test.py` |

---

## Notes for AI Assistants

### When Writing Code

1. **Always check context**: Use `request.session.get('current_organization_id')` to filter data
2. **Always check permissions**: Verify user ownership or membership before modifications
3. **Always use db_column**: Explicitly specify database column names
4. **Always use Czech**: User-facing text, URLs, messages
5. **Always add messages**: Provide feedback on success/error
6. **Always use get_object_or_404**: Better error handling
7. **Always specify db_table**: Required for all models

### When Reading Code

1. **Check model location**: Models are split into 21 files
2. **Check imports**: Models imported in `models/__init__.py`
3. **Check middleware**: `ModuleAccessMiddleware` may block URLs
4. **Check context processor**: Menu and context available globally
5. **Check URL names**: Use reverse() or {% url %} for links

### When Debugging

1. **Check logs**: `/var/log/uwsgi/fdk.log` or console output
2. **Check migrations**: `python manage.py showmigrations`
3. **Check database**: Verify data exists in MySQL
4. **Check session**: Print `request.session` dict
5. **Check permissions**: Print `OrganizationMembership` or `ProjectUser` queries

### When Proposing Changes

1. **Minimal changes**: Only change what's necessary
2. **Follow patterns**: Look at existing code for patterns
3. **Test thoroughly**: Check all affected views and templates
4. **Document changes**: Add comments for complex logic
5. **Consider context**: Will this work in both personal and org contexts?

---

## Version History

- **2025-12-04**: Initial CLAUDE.md created
- **2025-12-04**: Updated with modular model structure (21 files)
- **2025-12-04**: Added context switching documentation
- **2025-12-04**: Added subscription system details

---

**End of CLAUDE.md**

For questions or clarifications, refer to other documentation files or examine existing code patterns in the `/fdk_cz/` directory.
