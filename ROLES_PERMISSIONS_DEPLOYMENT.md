# 🔐 Deployment Guide: Comprehensive Roles & Permissions System

**Datum:** 2025-11-27
**Branch:** `claude/standardize-project-menu-01WXhZ1aj22HukucJ2JiJmRR`

---

## ✅ Co bylo implementováno:

### 1. **Rozšířený systém rolí a oprávnění**

Systém nyní podporuje tři úrovně rolí:
- **Projektové role** (project_owner, project_admin, project_manager, atd.)
- **Organizační role** (organization_owner, organization_admin, organization_member, organization_viewer)
- **Modulové role** (module_manager, module_editor, module_contributor, module_viewer)

### 2. **Nové databázové modely**

#### Organizační role:
- `OrganizationRole` - definice rolí v organizaci
- `OrganizationPermission` - oprávnění na úrovni organizace
- `OrganizationRolePermission` - vazební tabulka
- `OrganizationMembership` - změněna z CharField na ForeignKey

#### Modulové role:
- `ModuleRole` - role pro jednotlivé moduly
- `ModulePermission` - oprávnění v modulech (read, write, delete, manage)
- `ModuleRolePermission` - vazební tabulka
- `ModuleAccess` - přístup uživatele k modulu v rámci projektu/organizace

#### Projektové role - rozšířeno:
- Přidáno pole `description` pro lepší popis rolí
- Nové role: project_owner, project_controller, project_stakeholder, project_manager

### 3. **Management command**
- Aktualizován `init_roles` pro inicializaci všech rolí a oprávnění

---

## 📋 DEPLOYMENT INSTRUCTIONS

### Krok 1: Aktualizovat kód

```bash
cd /var/www/fdk.cz

# Fetch a checkout
git fetch origin
git checkout claude/standardize-project-menu-01WXhZ1aj22HukucJ2JiJmRR
git pull origin claude/standardize-project-menu-01WXhZ1aj22HukucJ2JiJmRR
```

### Krok 2: Aktivovat virtuální prostředí

```bash
source /var/www/fdk_app/fdk_env/bin/activate  # Upravit podle skutečné cesty
```

### Krok 3: Spustit migrace

```bash
cd /var/www/fdk.cz

# Spustit migrace ve správném pořadí
python manage.py migrate fdk_cz 0017_comprehensive_roles_permissions
```

### Krok 4: Inicializovat role a oprávnění

**DŮLEŽITÉ:** Tento krok MUSÍ proběhnout PŘED migrací 0018!

```bash
python manage.py init_roles
```

Tento příkaz vytvoří:
- ✅ 8 projektových rolí s 18 oprávněními
- ✅ 4 organizační role s 9 oprávněními
- ✅ 4 modulové role s 4 oprávněními

### Krok 5: Dokončit migrace

```bash
# Migrovat existující OrganizationMembership data
python manage.py migrate fdk_cz 0018_migrate_organization_membership_roles

# Finalizovat OrganizationMembership
python manage.py migrate fdk_cz 0019_finalize_organization_membership

# Nebo spustit všechny zbývající migrace najednou
python manage.py migrate
```

### Krok 6: Restartovat aplikaci

```bash
# Pro gunicorn
sudo systemctl restart gunicorn

# Nebo pro Apache
sudo systemctl restart apache2

# Nebo pro development server
# Ctrl+C a znovu python manage.py runserver
```

---

## 🔍 Ověření

Po deployment ověřte:

```bash
# 1. Zkontrolujte, že všechny role byly vytvořeny
python manage.py shell
>>> from fdk_cz.models import ProjectRole, OrganizationRole, ModuleRole
>>> ProjectRole.objects.count()  # Mělo by být 8
>>> OrganizationRole.objects.count()  # Mělo by být 4
>>> ModuleRole.objects.count()  # Mělo by být 4
>>> exit()

# 2. Zkontrolujte databázové tabulky
python manage.py dbshell
SELECT COUNT(*) FROM FDK_roles;  -- Projektové role
SELECT COUNT(*) FROM FDK_organization_roles;  -- Organizační role
SELECT COUNT(*) FROM FDK_module_roles;  -- Modulové role
\q
```

---

## 📊 Matice oprávnění

### Projektové role

| Role | View | Edit | Delete | Manage Users | Manage Budget | Create Tasks | Reports |
|------|------|------|--------|--------------|---------------|--------------|---------|
| **project_owner** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **project_admin** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **project_manager** | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **project_controller** | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **project_editor** | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **project_contributor** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **project_viewer** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **project_stakeholder** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### Organizační role

| Role | View | Edit | Delete | Manage Members | Create Projects | Manage Billing |
|------|------|------|--------|----------------|-----------------|----------------|
| **organization_owner** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **organization_admin** | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| **organization_member** | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **organization_viewer** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Modulové role

| Role | Read | Write | Delete | Manage |
|------|------|-------|--------|--------|
| **module_manager** | ✅ | ✅ | ✅ | ✅ |
| **module_editor** | ✅ | ✅ | ✅ | ❌ |
| **module_contributor** | ✅ | ✅ | ❌ | ❌ |
| **module_viewer** | ✅ | ❌ | ❌ | ❌ |

---

## 🎯 Použití v kódu

### Kontrola oprávnění v projektu

```python
from fdk_cz.models import ProjectUser, ProjectRolePermission

def user_has_project_permission(user, project, permission_name):
    """
    Zkontroluje, zda má uživatel v projektu dané oprávnění.
    """
    try:
        project_user = ProjectUser.objects.get(user=user, project=project)
        return ProjectRolePermission.objects.filter(
            role=project_user.role,
            permission__permission_name=permission_name
        ).exists()
    except ProjectUser.DoesNotExist:
        return False

# Použití
if user_has_project_permission(request.user, project, 'can_edit_project'):
    # Uživatel může editovat projekt
    pass
```

### Kontrola oprávnění v organizaci

```python
from fdk_cz.models import OrganizationMembership, OrganizationRolePermission

def user_has_org_permission(user, organization, permission_name):
    """
    Zkontroluje, zda má uživatel v organizaci dané oprávnění.
    """
    try:
        membership = OrganizationMembership.objects.get(
            user=user,
            organization=organization
        )
        return OrganizationRolePermission.objects.filter(
            role=membership.role,
            permission__permission_name=permission_name
        ).exists()
    except OrganizationMembership.DoesNotExist:
        return False

# Použití
if user_has_org_permission(request.user, org, 'can_manage_members'):
    # Uživatel může spravovat členy organizace
    pass
```

### Kontrola oprávnění v modulu

```python
from fdk_cz.models import ModuleAccess, ModuleRolePermission

def user_has_module_permission(user, module_name, project=None, organization=None, permission_name='can_read'):
    """
    Zkontroluje, zda má uživatel oprávnění k modulu.
    """
    try:
        access = ModuleAccess.objects.get(
            user=user,
            module_name=module_name,
            project=project,
            organization=organization
        )
        return ModuleRolePermission.objects.filter(
            role=access.role,
            permission__permission_name=permission_name
        ).exists()
    except ModuleAccess.DoesNotExist:
        return False

# Použití
if user_has_module_permission(request.user, 'warehouse', project=project, permission_name='can_write'):
    # Uživatel může zapisovat do skladu
    pass
```

### Dekorátor pro view

```python
from django.core.exceptions import PermissionDenied
from functools import wraps

def require_project_permission(permission_name):
    """
    Dekorátor pro view, který vyžaduje projektové oprávnění.
    Předpokládá, že view má parametr project_id.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, project_id, *args, **kwargs):
            from fdk_cz.models import Project
            project = Project.objects.get(project_id=project_id)

            if not user_has_project_permission(request.user, project, permission_name):
                raise PermissionDenied("Nemáte oprávnění k této akci.")

            return view_func(request, project_id, *args, **kwargs)
        return wrapper
    return decorator

# Použití
@require_project_permission('can_edit_project')
def edit_project(request, project_id):
    # View pro editaci projektu
    pass
```

---

## ⚠️ Důležité poznámky

1. **Pořadí migrací je kritické!**
   Nejprve 0017 → pak init_roles → pak 0018 → nakonec 0019

2. **Starý systém rolí**
   Staré hard-coded role v OrganizationMembership ('admin', 'member', 'viewer') budou automaticky migrovány na nové role

3. **Migrace existujících dat**
   Všechny existující organizační členství budou migrována:
   - 'admin' → 'organization_admin'
   - 'member' → 'organization_member'
   - 'viewer' → 'organization_viewer'

4. **Nové projekty**
   Pro nové projekty byste měli přiřazovat role jako 'project_owner', 'project_admin', atd.

5. **ModuleAccess**
   Modulové přístupy je potřeba přiřazovat manuálně podle potřeby. Nejsou automaticky vytvářeny.

---

## 🐛 Troubleshooting

### Problém: Migrace 0018 selhává

**Řešení:** Ujistěte se, že jste spustili `init_roles` PŘED migrací 0018.

```bash
python manage.py init_roles
python manage.py migrate fdk_cz 0018
```

### Problém: Chybí některé role

**Řešení:** Spusťte init_roles znovu - příkaz je idempotentní.

```bash
python manage.py init_roles
```

### Problém: OrganizationMembership.role je NULL

**Řešení:** Zkontrolujte, že migrace 0018 proběhla správně.

```bash
python manage.py migrate fdk_cz 0018 --fake  # pokud data už byla migrována manuálně
```

---

## 📞 Podpora

Pro otázky nebo problémy kontaktujte:
- GitHub Issues: [eKultura/fdk.cz](https://github.com/eKultura/fdk.cz/issues)
- Email: support@fdk.cz (upravit podle skutečnosti)

---

**Vytvořil:** Claude
**Datum:** 2025-11-27
