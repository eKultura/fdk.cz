# fdk.cz
Powerfull task management

# How to install

1. sudo apt install libmysqlclient-dev
2. pip3 install -r requirements.txt

[!TIP]
This one may also help: sudo pip3 install -U pip

# How to run it
1. rename settings_template.py -> settings.py
2. python3 manage.py migrate
3. python3 manage.py runserver

[!TIP]
If you running mysql locally use host 127.0.0.1 works better then localhost

Insert these roles into DB before creating project by running this command:


INSERT INTO `FDK_roles` (`role_id`, `role_name`) VALUES (2,    'Administrator'), (3,    'Editor'), (1,    'Owner'),(4,    'Viewer');

For summernotes to work add these to setting.py

INSTALLED_APPS = [
    ...
    'django_summernote',
]

SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
    },
}
=======
```python manage.py loaddata fixtures/FDK_roles.json```

or do it manually into DB

```INSERT INTO `FDK_roles` (`role_id`, `role_name`) VALUES (2,    'Administrator'), (3,    'Editor'), (1,    'Owner'),(4,    'Viewer');```

