# Models - Modulární struktura

Tento adresář obsahuje modely rozdělené do modulů podle views struktury.

## 📁 Struktura

Původní monolitický soubor `models.py` (2346 řádků) byl rozdělen do 20 modulů:

- `user.py` - ActivityLog, Users2
- `articles.py` - Article
- `company.py` - Company
- `organization.py` - Organization a související modely (Role, Permission, Membership)
- `project.py` - Project a všechny projektové modely (Task, Milestone, Document, Category, SWOT)
- `modules.py` - Moduly aplikace a předplatné
- `flist.py` - Flist, ListItem, ListPermission
- `contact.py` - Contact
- `warehouse.py` - Warehouse, WarehouseItem, WarehouseTransaction
- `contract.py` - Contract
- `test.py` - Test, TestError, TestScenario
- `accounting.py` - Invoice, JournalEntry, BalanceSheet
- `grants.py` - GrantProgram, GrantApplication
- `law.py` - Law, LawDocument, LawQuery
- `b2b.py` - B2BCompany, B2BContract, B2BDocument
- `hr.py` - Department, Employee
- `risk.py` - Risk
- `it.py` - ITAsset, ITIncident
- `asset.py` - Asset, AssetCategory
- `help.py` - HelpArticle

## 🔄 Jak to funguje

Soubor `__init__.py` importuje všechny modely z jednotlivých modulů, takže:

```python
from fdk_cz.models import Project, Organization, Invoice
```

Funguje **PŘESNĚ STEJNĚ** jako dříve!

## 🔙 Jak se vrátit zpět

Pokud je problém s novou strukturou:

1. Smazat/přejmenovat adresář `models/`
2. Přejmenovat `_models_old.py` zpět na `models.py`
3. Nebo použít zálohu `models_backup.py`

```bash
# Vrácení zpět:
mv fdk_cz/models fdk_cz/models_disabled
mv fdk_cz/_models_old.py fdk_cz/models.py
```

## ✅ Výhody

- ✓ Lepší organizace kódu
- ✓ Snazší navigace (modely podle funkcionality)
- ✓ Odpovídá struktuře views/
- ✓ Žádná změna v importech
- ✓ Kompatibilní se stávajícím kódem
