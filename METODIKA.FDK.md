# 📘 METODIKA VÝVOJE FDK.cz — ZÁSADY A PRAVIDLA

Tento dokument definuje závazné postupy pro architekturu, vývoj, styl kódu, bezpečnost a rozšiřování systému **FDK.cz**.
Slouží jako centrální metodika pro projekt, dostupná na `metodika.fdk`.

---

# 🏗️ 1. ARCHITEKTURA A MODULARITA

## 1.1 Primární principy
- Každá funkční oblast je implementována jako **samostatný modul**.
- Moduly jsou **maximálně nezávislé** a sdílí pouze společné modely a kontexty.
- Všechny moduly respektují **jednotnou adresářovou strukturu**.
- Každý modul má vlastní šablony, views a vlastní logiku – žádné zkratky.

## 1.2 Standardní struktura modulu

```
modul/
├── templates/modul/
│   ├── list_{entity}.html
│   ├── detail_{entity}.html
│   ├── edit_{entity}.html
│   ├── create_{entity}.html
│   └── delete_{entity}.html
├── views/
│   └── nazev_modulu.py
└── (modely jsou centralizované dle domén)
```

> **Views jsou vždy ve složce `views/` a pojmenované `nazev_modulu.py`.**
> Toto pravidlo je závazné pro všechny nové moduly.

## 1.3 URL a routing
- URL jednotlivých modulů se registrují v **centrálním `urls.py`**.
- Prefixy URL odpovídají názvu modulu:
  `/modul/…`
- Moduly nesmí přepisovat URL jiných modulů.
- URL musí být konzistentní a čitelné.

---

# ♻️ 2. RECYKLACE MODELŮ (DRY PRINCIP)

## 2.1 Zásada minimálního množství modelů
- Nový model vzniká pouze tehdy, pokud:
  - neexistuje odpovídající entita
  - nejde o podmnožinu existující entity
  - nejde o logické rozšíření existující struktury

## 2.2 Preferovaná architektura
- **ForeignKey** před novými entitami.
- **JSONField** pro flexibilní metadata.
- **M2M** jen pokud jde o skutečný vztah „mnoho na mnoho".

## 2.3 Společné kontexty ve všech modelech
Každý model musí uvažovat tyto vazby:

```python
organization = ForeignKey(Organization, null=True)
project = ForeignKey(Project, null=True)
owner = ForeignKey(User)
```

> Pokud model pracuje v rámci kontextu, musí podporovat všechny 3 roviny:
> **organizace → projekt → osobní**.

---

# 🎨 3. DESIGN, KÓD A ŠABLONY

## 3.1 Kódová čistota
- Minimalistický kód = nižší chybovost.
- Importy a metody jsou **abecedně seřazené**.
- Název souborů i metod odpovídá jejich účelu.
- Zakázáno používat inline styly.

## 3.2 Šablonový systém
- Všechny šablony používají **TailwindCSS**.
- Všechny mají strukturu:
  1. page title
  2. breadcrumbs
  3. action buttons
  4. obsah (table/detail/form)

- Responzivita je povinná.
- Ikony: pouze **HTML entity**, žádné externí knihovny.

## 3.3 Konzistence UI
- Jednotné barvy dle FDK designu.
- Jednotné rozmístění:
  - titulky
  - breadcrumbs
  - tabulka / detail
  - akce (tlačítka)

---

# 🔄 4. TROJJEDINÝ KONTEXT (ORGANIZACE–PROJEKT–OSOBA)

## 4.1 Tři roviny existence dat
Každá entita může existovat v jedné z těchto rovin:

1. **Organizační** – sdílené mezi uživateli dané organizace.
2. **Projektové** – vázané na konkrétní projekt.
3. **Osobní** – individuální data konkrétního uživatele.

## 4.2 Implementační pravidla
- Všechny modely musí mít nullable FK:
  ```python
  organization = models.ForeignKey(..., null=True, blank=True)
  project      = models.ForeignKey(..., null=True, blank=True)
  owner        = models.ForeignKey(User, on_delete=models.CASCADE)
  ```

## 4.3 Filtrování ve views
Data se filtrují podle aktuálního kontextu:
- aktuální organizace
- aktuální projekt
- aktuální uživatel

---

# 🚀 5. VÝVOJOVÝ WORKFLOW

## 5.1 Prioritizace (FDK zásada č. 1)
1. Funkčnost
2. Jednoduchost
3. Recyklace existujících komponent
4. UI a design

## 5.2 Postup vývoje modulů
1. Návrh modelové struktury
2. Návrh URL a views
3. Implementace základních šablon (list, detail, create, edit, delete)
4. Implementace logiky (CRUD)
5. Testování v reálném uživatelském scénáři
6. Vizuální doladění

## 5.3 Testování
- Testovací prostředí s aktivními moduly podle konfigurace.
- Testování probíhá:
  - interně vývojářem
  - interně týmem
  - v pilotním provozu
  - v produkci

---

# 📊 6. ROZŠIŘOVÁNÍ FUNKCÍ A BEZPEČNOST

## 6.1 Pravidla pro rozšiřování
- Vždy nejprve zhodnotit existující kód.
- Nové funkce musí být v souladu s architekturou.
- Nové moduly musí mít minimální závislosti.

## 6.2 Bezpečnost
Uživatel může vidět jen:
- data své organizace
- data svých projektů
- vlastní osobní data

Validace probíhá:
- ve views
- v modelech
- v šablonách

## 6.3 Audit
Každá důležitá entita musí mít:
```python
created_at
created_by
updated_at
updated_by
```

---

# 📦 7. DATOVÁ A KÓDOVÁ DOKUMENTACE

## 7.1 Verzování
- Každá úprava modelů → zápis do CHANGELOG.md
- Formát verzí:
  ```
  v{major}.{minor}.{patch}
  ```

## 7.2 Dokumentace modulů
Každý modul má svůj vlastní:
```
modul/README.md
```

Obsahuje:
- účel modulu
- strukturu
- datové vazby
- seznam šablon
- seznam URL
- logiku práv a rolí

---

# 🧩 8. ROZŠIŘUJÍCÍ SMĚRNICE

K doplnění později:
- Testovací scénáře
- Databázové verzování (migrations governance)
- CI validace
- UX guidelines
- Šablona pro návrh nového modulu

---

# ✔️ 9. Závěr

**Tato metodika je závazná pro vývoj celého systému FDK.cz.**

Zajišťuje:
- čistotu kódu
- škálovatelnost
- dlouhodobou udržitelnost

**Všechny budoucí moduly, úpravy a funkce se musí řídit tímto dokumentem.**
