# Metodika FDK.cz

## Drobečková navigace (Breadcrumbs)

Breadcrumbs musí být konzistentní na všech stránkách. Použij tento standardní formát:

### Základní formát

```html
<!-- Breadcrumbs -->
<nav style="margin-bottom: 1.5rem; font-size: 0.875rem;">
  <a href="{% url 'index' %}" style="color: #3b82f6; text-decoration: none;">Domů</a>
  <span style="color: #9ca3af; margin: 0 0.5rem;">→</span>
  <a href="{% url 'nazev_modulu' %}" style="color: #3b82f6; text-decoration: none;">Název modulu</a>
  <span style="color: #9ca3af; margin: 0 0.5rem;">→</span>
  <span style="color: #1e293b; font-weight: 500;">Aktuální stránka</span>
</nav>
```

### Pravidla

1. **Vždy začíná s "Domů"** - odkaz na `{% url 'index' %}`
2. **Oddělovač je →** - `<span style="color: #9ca3af; margin: 0 0.5rem;">→</span>`
3. **Odkazy jsou modré** - `color: #3b82f6; text-decoration: none;`
4. **Aktuální stránka není odkaz** - použij `<span>` s `font-weight: 500; color: #1e293b;`
5. **Umístění** - hned za `{% block content %}` na začátku

### Příklady podle modulů

#### Seznam položek
```
Domů → Modul → [Název seznamu]
```

#### Detail položky
```
Domů → Modul → [Seznam] → [Název položky]
```

#### Editace položky
```
Domů → Modul → [Seznam] → [Název položky] → Úprava
```

#### Vytvoření položky
```
Domů → Modul → [Seznam] → Nová položka
```

### Konkrétní příklady

| Stránka | Breadcrumbs |
|---------|-------------|
| Seznam kontaktů | Domů → Kontakty |
| Detail kontaktu | Domů → Kontakty → [Jméno kontaktu] |
| Editace kontaktu | Domů → Kontakty → [Jméno kontaktu] → Úprava |
| Seznam smluv | Domů → Smlouvy |
| Detail smlouvy | Domů → Smlouvy → [Název smlouvy] |
| Účetní deník | Domů → Účetnictví → Účetní deník |
| Rozvaha | Domů → Účetnictví → Počáteční/Konečná rozvaha |
| Detail účtu | Domů → Účetnictví → Účtová osnova → [Číslo účtu] |

---

## Zobrazování HTML obsahu

### Pravidlo |safe filtru

Pokud ukládáme obsah jako HTML nebo používáme markdown filter, **musíme použít |safe**:

```django
{{ object.description|markdown|safe }}
{{ object.title|safe }}
```

### Kde použít |safe

- Popisy (description) - vždy s `|markdown|safe`
- Titulky pokud obsahují HTML entity
- Komentáře s markdown formátováním

### Kde NEPOUŽÍVAT |safe

- Uživatelské vstupy bez sanitizace
- Data z nedůvěryhodných zdrojů

---

## Přesměrování po akcích

### Pravidla

1. **Po editaci** - vracet na seznam, ne na detail
2. **Po smazání** - vracet na seznam
3. **Po vytvoření** - vracet na detail nově vytvořené položky

### Příklady

```python
# Po editaci kontaktu
return redirect('my_contacts')

# Po smazání
return redirect('list_items')

# Po vytvoření
return redirect('detail_item', item_id=new_item.id)
```
