# 🚀 DEPLOYMENT INSTRUCTIONS - FDK.cz Subscription System

**Datum:** 2025-11-01
**Branch:** `claude/fix-fdk-organization-tool-011CUhgfyLGVueEjUT9JqgfW`

---

## ✅ Co bylo implementováno:

### 1. **Subscription systém (kompletní)**
- 5 databázových modelů (Module, UserModuleSubscription, ModuleBundle, Payment, ModuleUsage)
- Views pro správu předplatného
- Middleware pro kontrolu přístupu k placeným modulům
- Context processor pro dynamické menu
- Templates pro dashboard, pricing, nákup, zrušení

### 2. **Grants module enhancements**
- Rozšířené modely (GrantCall, GrantApplication)
- 2 nové modely (GrantOpportunityBookmark, GrantDocumentTemplate)
- Podpora externích integrací (DotaceEU, MŠMT)
- Lifecycle tracking

### 3. **ProjectRole fix**
- Management command `init_roles` pro inicializaci projektových rolí

---

## 📋 CO MUSÍŠ UDĚLAT NA SERVERU:

### Krok 1: Aktualizovat kód

```bash
cd /var/www/fdk.cz

# Fetch a checkout
git fetch origin
git checkout claude/fix-fdk-organization-tool-011CUhgfyLGVueEjUT9JqgfW
git pull origin claude/fix-fdk-organization-tool-011CUhgfyLGVueEjUT9JqgfW
```

### Krok 2: Aktualizovat settings.py

**DŮLEŽITÉ:** Zkopíruj změny z `config/settings_template.py` do `config/settings.py`:

```python
# Přidej na konec MIDDLEWARE:
MIDDLEWARE = [
    # ... existující ...
    'fdk_cz.middleware.module_access.ModuleAccessMiddleware',  # ← PŘIDAT
]

# Přidej do TEMPLATES context_processors:
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... existující ...
                'fdk_cz.context_processors.user_modules',  # ← PŘIDAT
            ],
        },
    },
]
```

### Krok 3: Spustit migrace

```bash
source env/bin/activate
python manage.py migrate
```

Mělo by vytvořit:
- Migration 0034: Subscription modely (5 tabulek)
- Migration 0035: Grants enhancements (2 tabulky + rozšíření)

### Krok 4: Inicializovat data

```bash
# Inicializovat projektové role (opraví chybu při vytváření projektů)
python manage.py init_roles

# Inicializovat moduly
python manage.py init_modules
```

### Krok 5: Restart serveru

```bash
# uWSGI
sudo systemctl restart uwsgi

# NEBO Gunicorn
sudo systemctl restart gunicorn

# NEBO
sudo systemctl restart fdk
```

### Krok 6: Vyčistit cache (pokud používáš)

```bash
python manage.py collectstatic --noinput
```

---

## 🎯 NOVÉ URL ENDPOINTY:

### Subscription URLs:
- `/predplatne/` - Dashboard předplatného
- `/ceny/` - Ceník modulů (veřejná stránka)
- `/predplatne/modul/<id>/objednat/` - Nákup modulu
- `/predplatne/<id>/zrusit/` - Zrušit předplatné
- `/predplatne/<id>/obnovit/` - Obnovit předplatné

### Stávající URLs fungují normálně:
- Projekty, úkoly, granty, testy, atd.

---

## 🔍 TESTOVÁNÍ:

### 1. Test vytvoření projektu
```
Přihlásit se → Projekty → Nový projekt
```
✅ Mělo by fungovat (opraveno init_roles)

### 2. Test subscription dashboardu
```
Přihlásit se → /predplatne/
```
✅ Mělo by zobrazit FREE moduly + dostupné PAID moduly

### 3. Test ceníku
```
/ceny/
```
✅ Mělo by zobrazit všechny moduly s cenami

### 4. Test nákupu modulu (DEMO režim)
```
/predplatne/ → Zakoupit modul → Vybrat typ → Aktivovat
```
✅ Mělo by okamžitě aktivovat bez platby (DEMO režim)

### 5. Test middleware (access control)
```
Pokus o přístup k /granty/ BEZ předplatného
```
✅ Mělo by přesměrovat na /ceny/ s varováním

---

## ⚙️ KONFIGURACE:

### Demo režim (momentálně aktivní):
- Moduly se aktivují OKAMŽITĚ bez platby
- Pro produkci: Implementovat Stripe/GoPay v `subscription.py`

### FREE moduly (dostupné všem):
1. Project Management
2. Task Management
3. Lists (do 10 seznamů)
4. Contacts

### PAID moduly (vyžadují předplatné):
- Granty a dotace (299 Kč/měsíc)
- Test Management (199 Kč/měsíc)
- Účetnictví (399 Kč/měsíc)
- Sklad (249 Kč/měsíc)
- Smlouvy (199 Kč/měsíc)
- Law AI (499 Kč/měsíc)
- HR Management (349 Kč/měsíc)
- B2B Management (349 Kč/měsíc)
- Risk Management (299 Kč/měsíc)
- IT Management + ITIL (449 Kč/měsíc)
- Asset Management (299 Kč/měsíc)

---

## 🐛 TROUBLESHOOTING:

### Problém: "ProjectRole matching query does not exist"
**Řešení:**
```bash
python manage.py init_roles
```

### Problém: Middleware chyby
**Řešení:** Zkontroluj že jsi přidal middleware do settings.py

### Problém: Templates se nenačítají
**Řešení:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart uwsgi
```

### Problém: Moduly se nezobrazují
**Řešení:**
```bash
python manage.py init_modules
# Restartovat server
```

---

## 📊 DATABÁZOVÉ TABULKY (nové):

1. `FDK_module` - Moduly systému
2. `FDK_user_module_subscription` - Předplatná uživatelů
3. `FDK_module_bundle` - Balíčky modulů
4. `FDK_payment` - Platby
5. `FDK_module_usage` - Analytics
6. `FDK_grant_opportunity_bookmark` - Bookmarky příležitostí
7. `FDK_grant_document_template` - Šablony dokumentů

**Rozšířené tabulky:**
- `FDK_grant_call` - Přidáno 9 sloupců (source, external_id, tags, atd.)
- `FDK_grant_application` - Přidáno 5 sloupců (lifecycle_stage, completion_percentage, atd.)

---

## ✉️ KONTAKT:

Pokud něco nefunguje, zkontroluj:
1. Migrace spuštěné? (`python manage.py migrate`)
2. Role inicializované? (`python manage.py init_roles`)
3. Moduly inicializované? (`python manage.py init_modules`)
4. Settings.py aktualizované? (middleware + context processor)
5. Server restartovaný?

---

**🎉 Hotovo! Subscription systém by měl fungovat.**

**DEMO režim:** Platby jsou simulované - vše se aktivuje okamžitě.

**Pro produkci:** Implementuj Stripe/GoPay podle `SUBSCRIPTION_SYSTEM_DESIGN.md`
