# fdk_cz/management/commands/init_modules.py

from django.core.management.base import BaseCommand
from fdk_cz.models import Module

class Command(BaseCommand):
    help = 'Inicializovat všechny moduly FDK systému s cenami'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Inicializace FDK modulů...'))

        modules_data = [
            # ============ FREE MODULY ============
            {
                'name': 'project_management',
                'display_name': 'Správa projektů',
                'display_name_en': 'Project Management',
                'description': 'Kompletní správa projektů s milníky, týmy, kategoriemi a dokumenty. Podporuje Agile/Scrum metodologie.',
                'short_description': 'Správa projektů',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'is_active': True,
                'url_patterns': ['/projekty/', '/project_', '/projects/'],
                'icon': '🛠️',
                'color': '#3b82f6',
                'order': 1
            },
            {
                'name': 'task_management',
                'display_name': 'Správa úkolů',
                'display_name_en': 'Task Management',
                'description': 'Správa úkolů pro projekty, týmy i jednotlivce. Podporuje subtasky, komentáře, přílohy a různé stavy.',
                'short_description': 'Úkoly a ToDo listy',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'is_active': True,
                'url_patterns': ['/ukoly/', '/task_', '/tasks/'],
                'icon': '✅',
                'color': '#10b981',
                'order': 2
            },
            {
                'name': 'lists',
                'display_name': 'Seznamy',
                'display_name_en': 'Lists',
                'description': 'Vlastní seznamy pro organizaci dat. Free verze umožňuje až 10 seznamů.',
                'short_description': 'Seznamy (do 10 zdarma)',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'is_active': True,
                'free_limit': 10,
                'url_patterns': ['/seznamy/', '/list_', '/lists/'],
                'icon': '📋',
                'color': '#8b5cf6',
                'order': 3
            },
            {
                'name': 'contacts',
                'display_name': 'Adresář kontaktů',
                'display_name_en': 'Address Book',
                'description': 'Správa kontaktů a adres pro projekty a organizace.',
                'short_description': 'Kontakty',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'is_active': True,
                'url_patterns': ['/kontakty/', '/contact', '/contacts/'],
                'icon': '👥',
                'color': '#06b6d4',
                'order': 4
            },

            # ============ PAID MODULY ============
            {
                'name': 'grants',
                'display_name': 'Granty a dotace',
                'display_name_en': 'Grants & Subsidies',
                'description': 'Kompletní životní cyklus dotací - vyhledávání příležitostí, příprava žádostí, správa dokumentů, reporting a monitoring.',
                'short_description': 'Granty a dotace',
                'price_monthly': 299,
                'price_yearly': 2990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/granty/', '/dotace/', '/grant_', '/grants/'],
                'icon': '💰',
                'color': '#f59e0b',
                'order': 10
            },
            {
                'name': 'test_management',
                'display_name': 'Test Management',
                'display_name_en': 'Test Management',
                'description': 'Testování aplikací, bug tracking, test reporting. Ideální pro QA týmy.',
                'short_description': 'Testování aplikací',
                'price_monthly': 199,
                'price_yearly': 1990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/testy/', '/test_', '/tests/'],
                'icon': '🧪',
                'color': '#ef4444',
                'order': 11
            },
            {
                'name': 'accounting',
                'display_name': 'Účetnictví',
                'display_name_en': 'Accounting',
                'description': 'Kompletní účetnictví s fakturací, DPH, automatickým číslováním faktur.',
                'short_description': 'Faktury a účetnictví',
                'price_monthly': 399,
                'price_yearly': 3990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/ucetnictvi/', '/accounting/', '/faktury/', '/invoice'],
                'icon': '📊',
                'color': '#14b8a6',
                'order': 12
            },
            {
                'name': 'warehouse',
                'display_name': 'Skladové hospodářství',
                'display_name_en': 'Warehouse Management',
                'description': 'Správa skladu, příjemky, výdejky, inventura, tracking pohybů zboží.',
                'short_description': 'Sklad',
                'price_monthly': 249,
                'price_yearly': 2490,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/sklad/', '/warehouse/'],
                'icon': '📦',
                'color': '#f97316',
                'order': 13
            },
            {
                'name': 'contracts',
                'display_name': 'Správa smluv',
                'display_name_en': 'Contract Management',
                'description': 'Správa smluv, dokumentů, výročí a upozornění na expirace.',
                'short_description': 'Smlouvy',
                'price_monthly': 199,
                'price_yearly': 1990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/smlouvy/', '/contract'],
                'icon': '📄',
                'color': '#6366f1',
                'order': 14
            },
            {
                'name': 'law_ai',
                'display_name': 'Legal Compliance & Law AI',
                'display_name_en': 'Legal Compliance & Law AI',
                'description': 'Právní compliance, AI asistent pro právní dotazy, databáze zákonů.',
                'short_description': 'Právo AI',
                'price_monthly': 499,
                'price_yearly': 4990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/pravo-ai/', '/law/', '/pravo/'],
                'icon': '⚖️',
                'color': '#8b5cf6',
                'order': 15
            },
            {
                'name': 'hr_management',
                'display_name': 'HR Management',
                'display_name_en': 'HR Management',
                'description': 'Správa zaměstnanců, docházka, mzdy, nábor, evidence dovolených.',
                'short_description': 'HR',
                'price_monthly': 349,
                'price_yearly': 3490,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/hr/', '/zamestnanci/'],
                'icon': '💼',
                'color': '#ec4899',
                'order': 16
            },
            {
                'name': 'b2b_management',
                'display_name': 'B2B Management',
                'display_name_en': 'B2B Management',
                'description': 'Správa B2B vztahů, obchodních příležitostí, CRM funkcionality.',
                'short_description': 'B2B',
                'price_monthly': 349,
                'price_yearly': 3490,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/b2b/', '/business/'],
                'icon': '🤝',
                'color': '#06b6d4',
                'order': 17
            },
            {
                'name': 'risk_management',
                'display_name': 'Správa rizik',
                'display_name_en': 'Risk Management',
                'description': 'Identifikace, hodnocení a správa rizik projektu nebo organizace.',
                'short_description': 'Rizika',
                'price_monthly': 299,
                'price_yearly': 2990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/rizika/', '/risk/'],
                'icon': '⚠️',
                'color': '#f59e0b',
                'order': 18
            },
            {
                'name': 'it_management',
                'display_name': 'Správa IT + ITIL',
                'display_name_en': 'IT Management + ITIL',
                'description': 'IT správa s ITIL procesy: Incident Management, Change Management, Problem Management, Service Design.',
                'short_description': 'IT Management + ITIL',
                'price_monthly': 449,
                'price_yearly': 4490,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/it/', '/sprava-it/', '/itil/'],
                'icon': '💻',
                'color': '#3b82f6',
                'order': 19
            },
            {
                'name': 'asset_management',
                'display_name': 'Správa majetku',
                'display_name_en': 'Asset Management',
                'description': 'Správa majetku organizace, inventarizace, odpisy, tracking.',
                'short_description': 'Majetek',
                'price_monthly': 299,
                'price_yearly': 2990,
                'is_free': False,
                'is_active': True,
                'url_patterns': ['/majetek/', '/asset/'],
                'icon': '🏢',
                'color': '#64748b',
                'order': 20
            },
        ]

        created_count = 0
        updated_count = 0

        for data in modules_data:
            module, created = Module.objects.update_or_create(
                name=data['name'],
                defaults=data
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Vytvořen modul: {module.display_name} ({module.name})'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'  🔄 Aktualizován modul: {module.display_name} ({module.name})'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'✅ HOTOVO! Vytvořeno: {created_count}, Aktualizováno: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'📊 Celkem modulů v databázi: {Module.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*60))

        # Statistiky
        free_modules = Module.objects.filter(is_free=True).count()
        paid_modules = Module.objects.filter(is_free=False).count()

        self.stdout.write('')
        self.stdout.write(f'  🆓 FREE moduly: {free_modules}')
        self.stdout.write(f'  💳 PAID moduly: {paid_modules}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 Systém je připraven k použití!'))
