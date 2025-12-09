# Session Context Debug Guide

## Problém
Sidebar ukazuje "Osobní režim" i po přepnutí do organizace

## Diagnostika

### 1. Zkontroluj settings.py na serveru
```bash
ssh na_server
cd /var/www/fdk.cz
grep -A5 "SESSION_" config/settings.py
```

**Mělo by být:**
```python
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

**Pokud to tam NENÍ**, přidej to a restartuj server:
```bash
nano config/settings.py
# Přidej session nastavení z settings_template.py
sudo systemctl restart gunicorn  # nebo uwsgi
```

### 2. Zkontroluj session tabulku
```bash
mysql -u fdk_user -p fdk_db
```
```sql
SELECT COUNT(*) FROM django_session;
SELECT * FROM django_session WHERE expire_date > NOW() LIMIT 5;
```

### 3. Vymaž cache a session cookies v prohlížeči
- Chrome: F12 → Application → Clear storage → Clear site data
- Firefox: F12 → Storage → Cookies → Delete all

### 4. Test session persistence
Navštiv: `https://fdk.cz/debug-session/`
- Mělo by ukázat všechna session data
- Zkontroluj, jestli tam je `current_organization_id`

### 5. Zkontroluj logy
```bash
tail -f /var/log/gunicorn/fdk.log | grep "CONTEXT SWITCH"
```

Při přepnutí organizace bys měl vidět:
```
CONTEXT SWITCH: User xxx switched to org InveLIB (ID: 123)
Session key 'current_organization_id' = 123
```

A pak při načtení další stránky:
```
CONTEXT PROCESSOR CALLED
Current org ID from session: 123
User xxx in org context: InveLIB
```

## Rychlá oprava
Pokud nic nefunguje, zkus:
```bash
cd /var/www/fdk.cz
git pull
cp config/settings_template.py config/settings.py
# Uprav SECRET_KEY, DB credentials atd.
python manage.py migrate  # případně
sudo systemctl restart gunicorn
```

## Pokud to pořád nefunguje
Pravděpodobně je problém s:
1. **Multiple gunicorn workers** - session se nesynchronizuje
2. **Cached pages** - Django cache middleware
3. **Reverse proxy cache** - nginx cache

Zkus:
```bash
# Restart všeho
sudo systemctl restart nginx
sudo systemctl restart gunicorn
# Vymaž Django cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```
