# 🔐 Průvodce systémem rolí a oprávnění

## 📖 Úvod

Systém FDK.cz používá třístupňový systém rolí a oprávnění:
1. **Organizační role** - oprávnění na úrovni celé organizace
2. **Projektové role** - oprávnění na úrovni konkrétního projektu
3. **Modulové role** - granulární oprávnění pro jednotlivé moduly (sklad, kontakty, faktury, atd.)

---

## 🏢 Organizační role

### organization_owner (Vlastník organizace)
**Kdy použít:** Pro zakládatele nebo majitele organizace

**Oprávnění:**
- ✅ Kompletní kontrola nad organizací
- ✅ Může smazat organizaci
- ✅ Spravuje všechny členy
- ✅ Spravuje fakturaci
- ✅ Přístup ke všem projektům
- ✅ Může vytvářet a spravovat projekty

**Příklad použití:**
```python
from fdk_cz.models import OrganizationMembership, OrganizationRole

# Přiřadit uživatele jako ownera organizace
owner_role = OrganizationRole.objects.get(role_name='organization_owner')
OrganizationMembership.objects.create(
    user=user,
    organization=organization,
    role=owner_role
)
```

---

### organization_admin (Administrátor organizace)
**Kdy použít:** Pro hlavní správce, kteří pomáhají řídit organizaci

**Oprávnění:**
- ✅ Upravuje nastavení organizace
- ✅ Spravuje členy (přidává/odebírá)
- ✅ Vytváří a spravuje projekty
- ✅ Přístup ke všem projektům
- ❌ Nemůže smazat organizaci
- ❌ Nemůže spravovat fakturaci

**Rozdíl oproti owner:**
Nemůže smazat organizaci ani spravovat platby/fakturaci.

---

### organization_member (Člen organizace)
**Kdy použít:** Pro běžné zaměstnance nebo spolupracovníky

**Oprávnění:**
- ✅ Vidí organizaci a její projekty
- ✅ Může vytvářet nové projekty
- ❌ Nemůže upravovat organizaci
- ❌ Nemůže spravovat členy

**Příklad:**
Vývojář, který pracuje na projektech organizace.

---

### organization_viewer (Pozorovatel organizace)
**Kdy použít:** Pro externí spolupracovníky, auditora, apod.

**Oprávnění:**
- ✅ Vidí organizaci
- ✅ Vidí všechny projekty (read-only)
- ❌ Nemůže vytvářet projekty
- ❌ Nemůže nic upravovat

**Příklad:**
Externí auditor, který potřebuje nahlédnout do projektů.

---

## 📁 Projektové role

### project_owner (Vlastník projektu)
**Kdy použít:** Pro osobu zodpovědnou za projekt

**Oprávnění:**
- ✅ Kompletní kontrola nad projektem
- ✅ Může smazat projekt
- ✅ Spravuje uživatele projektu
- ✅ Spravuje rozpočet
- ✅ Všechna oprávnění k úkolům, dokumentům, milníkům

---

### project_admin (Administrátor projektu)
**Kdy použít:** Pro zástupce PM nebo vedoucí týmu

**Oprávnění:**
- ✅ Upravuje projekt
- ✅ Spravuje uživatele
- ✅ Spravuje rozpočet
- ✅ Všechna oprávnění k obsahu
- ❌ Nemůže smazat projekt

**Rozdíl oproti owner:**
Nemůže smazat projekt.

---

### project_manager (Projektový manažer)
**Kdy použít:** Pro projektového manažera, který řídí projekt

**Oprávnění:**
- ✅ Upravuje projekt
- ✅ Spravuje rozpočet
- ✅ Vytváří a přiřazuje úkoly
- ✅ Spravuje milníky
- ✅ Vytváří reporty
- ❌ Nemůže spravovat uživatele

**Typický use case:**
PM, který řídí projekt, ale nepřidává/neodebírá členy týmu.

---

### project_controller (Kontrolor projektu)
**Kdy použít:** Pro finanční kontrolora nebo auditora

**Oprávnění:**
- ✅ Vidí projekt (read-only)
- ✅ Spravuje rozpočet
- ✅ Vytváří reporty
- ❌ Nemůže upravovat obsah projektu

**Typický use case:**
Finanční controller, který sleduje čerpání rozpočtu.

---

### project_editor (Editor projektu)
**Kdy použít:** Pro aktivní členy týmu

**Oprávnění:**
- ✅ Upravuje projekt
- ✅ Vytváří a upravuje úkoly
- ✅ Vytváří a upravuje dokumenty
- ✅ Vytváří a upravuje milníky
- ❌ Nemůže spravovat rozpočet
- ❌ Nemůže spravovat uživatele

**Typický use case:**
Vývojář nebo designer, který aktivně pracuje na projektu.

---

### project_contributor (Přispěvatel)
**Kdy použít:** Pro příležitostné přispěvatele

**Oprávnění:**
- ✅ Vidí projekt
- ✅ Vytváří úkoly
- ✅ Upravuje úkoly (pravděpodobně jen své)
- ✅ Vytváří dokumenty
- ❌ Nemůže upravovat projekt
- ❌ Nemůže mazat

**Typický use case:**
Externí freelancer, který přispívá do projektu.

---

### project_viewer (Pozorovatel)
**Kdy použít:** Pro osoby, které potřebují jen sledovat projekt

**Oprávnění:**
- ✅ Vidí projekt (read-only)
- ✅ Vidí reporty
- ❌ Nemůže nic upravovat

**Typický use case:**
Klient nebo stakeholder, který chce sledovat postup.

---

### project_stakeholder (Stakeholder)
**Kdy použít:** Pro klíčové stakeholdery projektu

**Oprávnění:**
- ✅ Vidí projekt (read-only)
- ✅ Vidí reporty
- ❌ Nemůže nic upravovat

**Rozdíl oproti viewer:**
Logické oddělení - stakeholder je významnější osoba (investor, klient, vedení).

---

## 🔧 Modulové role

Modulové role se přiřazují **pro konkrétní modul** (warehouse, contact, invoice, atd.) v rámci **projektu nebo organizace**.

### Dostupné moduly:
- `warehouse` - Sklad
- `contact` - Kontakty
- `invoice` - Faktury
- `task` - Úkoly
- `document` - Dokumenty
- `milestone` - Milníky

### module_manager (Správce modulu)
**Oprávnění:**
- ✅ Read (čtení)
- ✅ Write (zápis)
- ✅ Delete (mazání)
- ✅ Manage (správa - např. nastavení, export, import)

**Příklad:**
Jan má roli "module_manager" pro modul "warehouse" v projektu X.
→ Jan může dělat cokoliv se skladem v projektu X.

---

### module_editor (Editor modulu)
**Oprávnění:**
- ✅ Read
- ✅ Write
- ✅ Delete
- ❌ Manage

**Příklad:**
Petra má roli "module_editor" pro modul "invoice" v organizaci Y.
→ Petra může vytvářet, upravovat a mazat faktury v organizaci Y, ale nemůže měnit nastavení fakturace.

---

### module_contributor (Přispěvatel modulu)
**Oprávnění:**
- ✅ Read
- ✅ Write
- ❌ Delete
- ❌ Manage

**Příklad:**
Tomáš má roli "module_contributor" pro modul "contact" v projektu Z.
→ Tomáš může přidávat a upravovat kontakty, ale nemůže je mazat.

---

### module_viewer (Pozorovatel modulu)
**Oprávnění:**
- ✅ Read
- ❌ Write
- ❌ Delete
- ❌ Manage

**Příklad:**
Marie má roli "module_viewer" pro modul "warehouse" v projektu X.
→ Marie vidí sklad, ale nemůže nic měnit.

---

## 🎯 Praktické příklady použití

### Příklad 1: Startupová firma

**Organizace:** "TechStartup s.r.o."

**Členové:**
- Jan (Founder) → `organization_owner`
- Petra (CTO) → `organization_admin`
- Tomáš (Developer) → `organization_member`
- Marie (Investor) → `organization_viewer`

**Projekt:** "MVP Aplikace"

**Členové projektu:**
- Jan → `project_owner`
- Petra → `project_manager`
- Tomáš → `project_editor`
- Marie → `project_stakeholder`

**Modulové přístupy:**
- Tomáš má `module_manager` pro modul `task` (spravuje úkoly)
- Petra má `module_manager` pro modul `warehouse` (spravuje sklad)
- Marie má `module_viewer` pro modul `invoice` (vidí faktury)

---

### Příklad 2: Agentura s klienty

**Organizace:** "WebAgency s.r.o."

**Členové:**
- Alice (Owner) → `organization_owner`
- Bob (PM) → `organization_admin`
- Carol (Designer) → `organization_member`
- David (Developer) → `organization_member`

**Projekt:** "Web pro Klienta A"

**Členové projektu:**
- Alice → `project_owner`
- Bob → `project_manager`
- Carol → `project_editor`
- David → `project_editor`
- Klient → `project_viewer`

**Modulové přístupy:**
- Bob má `module_manager` pro všechny moduly
- Carol má `module_editor` pro `task` a `document`
- David má `module_editor` pro `task`
- Klient má `module_viewer` pro `document` a `milestone`

---

### Příklad 3: Vládní/veřejný projekt s auditorem

**Organizace:** "MěstoXY"

**Projekt:** "Digitalizace úřadu"

**Členové:**
- Vedoucí IT → `project_owner`
- Projektový manažer → `project_manager`
- Finanční controller → `project_controller` (sleduje rozpočet)
- Externí auditor → `project_viewer`
- Subdodavatelé → `project_contributor`

**Modulové přístupy:**
- Controller má `module_manager` pro modul `invoice`
- Auditor má `module_viewer` pro všechny moduly
- Subdodavatelé mají `module_contributor` pro modul `task`

---

## 💡 Tipy a best practices

### 1. Princip minimálních oprávnění
Vždy přiřazujte **nejnižší možnou roli**, která je pro uživatele potřebná.

### 2. Kombinace rolí
Uživatel může mít:
- 1 roli v organizaci
- Různé role v různých projektech
- Různé modulové role v různých projektech/organizacích

### 3. Hierarchie oprávnění
```
organization_owner > project_owner > module_manager
```

Pokud má uživatel `organization_owner`, měl by mít přístup ke všem projektům.
Pokud má `project_owner`, měl by mít přístup ke všem modulům projektu.

### 4. Kdy použít modulové role?
Modulové role jsou užitečné, když:
- Chcete udělit přístup jen k určité části projektu
- Máte externího spolupracovníka, který pracuje jen se skladem
- Chcete omezit přístup k citlivým datům (faktury)

### 5. Organizace vs. Projekt
- **Organizace** = firma, instituce
- **Projekt** = konkrétní zakázka, iniciativa

Uživatel může být členem organizace, ale nemusí být přiřazen ke všem projektům.

---

## 🔒 Bezpečnostní doporučení

1. **Pravidelný audit oprávnění**
   Pravidelně kontrolujte, kdo má jaké role, zejména `owner` a `admin`.

2. **Odebírejte oprávnění po odchodu**
   Když člověk opustí projekt/organizaci, ihned odeberte jeho členství.

3. **Dokumentujte důvody**
   Zaznamenávejte, proč byla určitá role přidělena.

4. **Dvě oči vidí více**
   Pro kritické operace (mazání projektu, fakturace) mějte vždy více než jednoho ownera.

---

## 📝 FAQ

**Q: Jaký je rozdíl mezi project_viewer a project_stakeholder?**
A: Funkčně jsou stejné (read-only přístup). Stakeholder je logické oddělení pro významné osoby (investor, klient, vedení).

**Q: Může mít uživatel více rolí v jednom projektu?**
A: Ne, každý uživatel má v projektu právě jednu roli (ProjectUser.role).

**Q: Co když potřebuji custom oprávnění?**
A: Můžete vytvořit novou roli a přiřadit jí potřebná oprávnění, nebo použít modulové role pro granulární kontrolu.

**Q: Jak změnit roli uživatele?**
A: Upravte ProjectUser nebo OrganizationMembership objekt a změňte hodnotu `role`.

```python
project_user = ProjectUser.objects.get(user=user, project=project)
new_role = ProjectRole.objects.get(role_name='project_editor')
project_user.role = new_role
project_user.save()
```

---

**Vytvořil:** Claude
**Datum:** 2025-11-27
**Verze:** 1.0
