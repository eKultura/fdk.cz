# Email Setup - FDK.cz

## Přehled

FDK.cz používá tři email adresy pro různé typy automatické komunikace:

- **noreply@fdk.cz** - Automatické notifikace (přiřazení úkolů, pozvánky do projektů)
- **info@fdk.cz** - Obecná komunikace
- **support@fdk.cz** - Uživatelská podpora

## Nastavení emailových schránek

### 1. Vytvoření schránek na Seznam.cz

1. Přejděte na [email.seznam.cz](https://email.seznam.cz)
2. Vytvořte tři nové emailové schránky:
   - `noreply@fdk.cz`
   - `info@fdk.cz`
   - `support@fdk.cz`

### 2. Povolení SMTP přístupu

Pro každou schránku:

1. Přihlaste se do schránky
2. Přejděte do **Nastavení** → **SMTP/IMAP**
3. Povolte **SMTP přístup**
4. Poznamenejte si hesla pro každou schránku

### 3. Konfigurace .env souboru

1. Zkopírujte `.env.example` na `.env`:
   ```bash
   cp .env.example .env
   ```

2. Vyplňte email credentials do `.env`:
   ```bash
   # No-reply email
   FDK_NOREPLY_EMAIL=noreply@fdk.cz
   FDK_NOREPLY_PASSWORD=vaše-heslo-pro-noreply

   # Info email
   FDK_INFO_EMAIL=info@fdk.cz
   FDK_INFO_PASSWORD=vaše-heslo-pro-info

   # Support email
   FDK_SUPPORT_EMAIL=support@fdk.cz
   FDK_SUPPORT_PASSWORD=vaše-heslo-pro-support
   ```

3. Nastavte URL webu:
   ```bash
   SITE_URL=https://fdk.cz
   ```

### 4. Restartování aplikace

Po úpravě `.env` restartujte Django aplikaci:

```bash
# Pro development
python manage.py runserver

# Pro production (systemd)
sudo systemctl restart fdk
```

## Typy emailů

### 1. Pozvánka do projektu (noreply@fdk.cz)

**Kdy se posílá:** Když je uživatel přidán do projektu a nemá účet

**Šablona:**
- HTML: `templates/emails/project_invitation.html`
- Text: `templates/emails/project_invitation.txt`

**Funkce:** `fdk_cz.utils.email.send_project_invitation_email()`

**Obsah:**
- Jméno projektu
- Role uživatele
- Odkaz na registraci s předvyplněným emailem
- Kdo poslal pozvánku

### 2. Přidání do projektu (noreply@fdk.cz)

**Kdy se posílá:** Když je existující uživatel přidán do projektu

**Šablona:**
- HTML: `templates/emails/project_member_added.html`
- Text: `templates/emails/project_member_added.txt`

**Funkce:** `fdk_cz.utils.email.send_project_member_added_email()`

**Obsah:**
- Jméno projektu
- Role uživatele
- Přímý odkaz na projekt
- Kdo přidal uživatele

### 3. Přiřazení úkolu (noreply@fdk.cz)

**Kdy se posílá:** Když je uživateli přiřazen úkol

**Šablona:**
- HTML: `templates/emails/task_assigned.html`
- Text: `templates/emails/task_assigned.txt`

**Funkce:** `fdk_cz.utils.email.send_task_assignment_email()`

**Obsah:**
- Název úkolu
- Popis úkolu
- Priorita, status, termín
- Přímý odkaz na úkol
- Odkaz na nastavení notifikací

## Použití v kódu

### Poslání pozvánky do projektu

```python
from fdk_cz.utils.email import send_project_invitation_email

send_project_invitation_email(
    email='uzivatel@example.com',
    project=project_instance,
    role=role_instance,
    invited_by=request.user
)
```

### Notifikace o přidání do projektu

```python
from fdk_cz.utils.email import send_project_member_added_email

send_project_member_added_email(
    user=user_instance,
    project=project_instance,
    role=role_instance,
    added_by=request.user
)
```

### Notifikace o přiřazení úkolu

```python
from fdk_cz.utils.email import send_task_assignment_email

send_task_assignment_email(
    user=assigned_user,
    task=task_instance,
    project=project_instance,
    assigned_by=request.user
)
```

## SMTP Konfigurace (Seznam.cz)

**Server:** smtp.seznam.cz
**Port:** 465
**Zabezpečení:** SSL
**Autentizace:** Email + heslo

## Testování emailů

Pro testování odesílání emailů můžete použít:

```bash
python manage.py shell
```

```python
from fdk_cz.utils.email import send_email

send_email(
    recipient='vas-email@example.com',
    subject='Test email',
    html_content='<h1>Test</h1><p>Toto je testovací email</p>',
    text_content='Test\n\nToto je testovací email'
)
```

## Řešení problémů

### Email se neposílá

1. **Zkontrolujte .env:**
   - Je soubor `.env` v root adresáři?
   - Jsou vyplněny všechny email credentials?

2. **Zkontrolujte SMTP přístup:**
   - Je povolený SMTP přístup v nastavení Seznam.cz schránky?
   - Je heslo správné?

3. **Zkontrolujte logy:**
   ```bash
   # Production logs
   sudo journalctl -u fdk -f

   # Development logs
   # Hledejte [✔] nebo [✖] zprávy v konzoli
   ```

### Email dorazí jako spam

1. Nastavte SPF záznam v DNS:
   ```
   v=spf1 include:_spf.seznam.cz ~all
   ```

2. Nastavte DKIM pro doménu fdk.cz v administraci Seznam.cz

3. Nastavte DMARC záznam:
   ```
   v=DMARC1; p=none; rua=mailto:postmaster@fdk.cz
   ```

## Dodatečné informace

- Všechny emaily mají HTML i textovou verzi (fallback)
- Šablony podporují Django template systém
- Patička obsahuje odkaz na odhlášení z notifikací
- Všechny odkazy vedou na SITE_URL z .env
