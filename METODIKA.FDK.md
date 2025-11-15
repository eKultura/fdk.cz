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

## 3.4 Pravidla pojmenování

### **ZÁSADNÍ PRAVIDLO: Vše v angličtině**

- **Soubory šablon**: POUZE anglické názvy
  ```
  ✅ SPRÁVNĚ: detail_contract.html, list_employees.html
  ❌ ŠPATNĚ: detail_smlouvy.html, seznam_zamestnancu.html
  ```

- **URL názvy**: anglické výrazy
  ```python
  ✅ SPRÁVNĚ: path('contract/<int:pk>/', ...)
  ❌ ŠPATNĚ: path('smlouva/<int:pk>/', ...)
  ```

- **Proměnné a funkce**: snake_case, anglicky
  ```python
  ✅ SPRÁVNĚ: def create_employee(request):
  ❌ ŠPATNĚ: def vytvor_zamestnance(request):
  ```

- **Modely a třídy**: PascalCase, anglicky
  ```python
  ✅ SPRÁVNĚ: class Employee(models.Model):
  ❌ ŠPATNĚ: class Zamestnanec(models.Model):
  ```

### Výjimky z pravidla:
- Komentáře v kódu mohou být česky pro srozumitelnost týmu
- UI texty (label, help_text) jsou česky pro koncové uživatele
- Dokumentace může být česky

## 3.5 Tabulky - jednotný styl a responsivita

### Základní pravidla:
- **VŽDY** obalit tabulku v `<div class="overflow-x-auto">` - KRITICKÉ pro responzivitu!
- Používat třídu `data-table` pro jednotný styl
- Responzivní sloupce: `hidden md:table-cell`, `hidden lg:table-cell`
- Akce vpravo: `text-right` třída na poslední sloupec
- Každá tabulka je v **bílém boxu** s padding a stínem

### Vzorová struktura (POUŽÍT VŠUDE):

```html
<!-- Card wrapper (volitelné, ale doporučené) -->
<div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Název tabulky</h2>

    <!-- POVINNÝ overflow wrapper - zabraňuje přetékání -->
    <div class="overflow-x-auto">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Hlavní sloupec (vždy viditelný)</th>
                    <th class="hidden md:table-cell">Tablet+ (768px+)</th>
                    <th class="hidden lg:table-cell">Desktop (1024px+)</th>
                    <th class="text-right">Akce</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <strong>Primární data</strong>
                        <div class="text-xs text-gray-500 mt-1">Pomocné info na mobilu</div>
                    </td>
                    <td class="hidden md:table-cell">Data</td>
                    <td class="hidden lg:table-cell">Data</td>
                    <td class="text-right">
                        <div class="data-table-actions">
                            <a href="#">👁️ Detail</a>
                            <a href="#">✏️ Upravit</a>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Empty state (když není žádná data) -->
    {% if not items %}
    <div style="text-align: center; padding: 3rem; background: #f8fafc; border-radius: 8px;">
        <span style="font-size: 3rem; display: block; margin-bottom: 0.5rem;">📋</span>
        <p style="color: #64748b;">Žádná data k zobrazení</p>
    </div>
    {% endif %}
</div>
```

### Povinné vlastnosti:
- `overflow-x-auto` - **KRITICKÉ!** Musí být na wrapperu kolem každé tabulky
- `data-table` - třída pro automatické styly tabulky
- `hidden md:table-cell` - skrýt sloupce na mobilu (< 768px)
- `hidden lg:table-cell` - skrýt sloupce na tabletu (< 1024px)
- `text-right` - zarovnání akcí vpravo
- `data-table-actions` - wrapper pro akční tlačítka

### Responzivní strategie:
1. **Mobil (< 768px)**: Zobrazit pouze nejdůležitější sloupce
2. **Tablet (768px+)**: Zobrazit střední prioritu
3. **Desktop (1024px+)**: Zobrazit všechny sloupce

### CSS třída data-table (v base.css):
Automaticky aplikuje jednotný styl na všechny tabulky:
- Šedé pozadí hlavičky
- Hover efekt na řádcích
- Správný padding a zarovnání
- Dělící čáry mezi řádky

## 3.6 Formuláře - jednotný styl

### Základní pravidla:
- Formuláře v **bílém boxu** s padding
- Jednotné styly pro všechny input prvky
- Jasné označení povinných polí

### Standardní struktura formuláře:

```html
<div class="bg-white rounded-lg shadow-md p-6">
    <form method="post">
        {% csrf_token %}

        <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="field_name">
                Název pole <span class="text-red-500">*</span>
            </label>
            <input
                type="text"
                id="field_name"
                name="field_name"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
            >
        </div>

        <!-- Další pole -->

        <div class="flex justify-end space-x-2 mt-6">
            <a href="{% url 'list_url' %}"
               class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400">
                Zrušit
            </a>
            <button type="submit"
                    class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                Uložit
            </button>
        </div>
    </form>
</div>
```

### Povinné vlastnosti formulářů:
- `bg-white rounded-lg shadow-md p-6` - bílý box s padding
- `mb-4` - mezera mezi poli
- `text-red-500` - označení povinných polí hvězdičkou
- `focus:ring-2 focus:ring-blue-500` - focus stav inputů
- Tlačítka vždy v pravém dolním rohu

## 3.7 Tlačítka - umístění, styly, marginy

### Hierarchie tlačítek:

```html
<!-- Primární akce (modrá) -->
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
    Uložit
</button>

<!-- Sekundární akce (šedá) -->
<button class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500">
    Zrušit
</button>

<!-- Destruktivní akce (červená) -->
<button class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500">
    Smazat
</button>

<!-- Pozitivní akce (zelená) -->
<button class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500">
    Schválit
</button>
```

### Umístění tlačítek:

**1. V hlavičce stránky (action buttons):**
```html
<div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold">Nadpis</h1>
    <div class="flex space-x-2">
        <a href="..." class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            + Přidat nový
        </a>
    </div>
</div>
```

**2. V tabulkách (akce na řádku):**
```html
<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
    <div class="flex space-x-2">
        <a href="..." class="text-blue-600 hover:text-blue-900">Detail</a>
        <a href="..." class="text-green-600 hover:text-green-900">Upravit</a>
        <a href="..." class="text-red-600 hover:text-red-900">Smazat</a>
    </div>
</td>
```

**3. Ve formulářích (tlačítka submit):**
```html
<div class="flex justify-end space-x-2 mt-6">
    <a href="..." class="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400">Zrušit</a>
    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Uložit</button>
</div>
```

### Marginy a spacing:
- Mezi tlačítky: `space-x-2` (horizontální mezera)
- Pod nadpisem: `mb-6`
- Nad tlačítky ve formuláři: `mt-6`
- Uvnitř tlačítka: `px-4 py-2` (padding)

## 3.8 Responzivní tabulky - JEDNOTNÝ STANDARD

### KRITICKÉ PRAVIDLO:
**KAŽDÁ TABULKA MUSÍ BÝT ZABALENÁ V `<div class="overflow-x-auto">`**

Toto je POVINNÉ pro všechny tabulky v systému, aby se zabránilo přetékání tabulek přes okraj stránky na mobilních zařízeních.

### Standardní struktura responzivní tabulky:

```html
<!-- SPRÁVNĚ: Tabulka s overflow wrapperem -->
<div class="content-card">
    <h3>Nadpis tabulky</h3>

    <div class="overflow-x-auto">
    <table class="data-table">
        <thead>
            <tr>
                <th>Sloupec 1</th>
                <th class="hidden md:table-cell">Sloupec 2 (skrytý na mobilu)</th>
                <th class="text-right">Akce</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Data</td>
                <td class="hidden md:table-cell">Data 2</td>
                <td class="text-right">
                    <div class="data-table-actions">
                        <a href="#">Detail</a>
                        <a href="#">Upravit</a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    </div>
</div>
```

### Povinné vlastnosti:

1. **Overflow wrapper**
   - VŽDY obalit `<table>` v `<div class="overflow-x-auto">`
   - Wrapper musí být uvnitř `.content-card`, ale venku z nadpisu

2. **Responzivní sloupce**
   - Méně důležité sloupce: `class="hidden md:table-cell"`
   - Důležité sloupce: bez hidden třídy
   - Minimálně 2-3 sloupce musí být viditelné na mobilu

3. **Table class**
   - Použít `class="data-table"` pro jednotný styl

4. **Akce v pravém sloupci**
   - Sloupec s akcemi: `class="text-right"`
   - Akce zabalit v `<div class="data-table-actions">`

### Příklady chyb:

```html
<!-- ❌ ŠPATNĚ: Bez overflow wrapperu -->
<div class="content-card">
    <h3>Tabulka</h3>
    <table class="data-table">
        <!-- Tabulka přeteče na mobilu! -->
    </table>
</div>

<!-- ✅ SPRÁVNĚ: S overflow wrapperem -->
<div class="content-card">
    <h3>Tabulka</h3>
    <div class="overflow-x-auto">
    <table class="data-table">
        <!-- Tabulka bude scrollovatelná na mobilu -->
    </table>
    </div>
</div>
```

### Kontrolní seznam:
- [ ] Tabulka je zabalená v `<div class="overflow-x-auto">`
- [ ] Wrapper je UVNITŘ `.content-card`
- [ ] Wrapper je KOLEM `<table>`, ne kolem celého content-cardu
- [ ] Méně důležité sloupce mají `hidden md:table-cell`
- [ ] Tabulka používá `class="data-table"`

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
