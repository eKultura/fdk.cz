# fdk_cz/management/commands/init_roles.py

from django.core.management.base import BaseCommand
from fdk_cz.models import (
    # Projektové role
    ProjectRole, ProjectPermission, ProjectRolePermission,
    # Organizační role
    OrganizationRole, OrganizationPermission, OrganizationRolePermission,
    # Modulové role
    ModuleRole, ModulePermission, ModuleRolePermission
)

class Command(BaseCommand):
    help = 'Inicializovat všechny role a oprávnění (projekt, organizace, moduly)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🔐 Inicializace rolí a oprávnění...'))
        self.stdout.write('')

        # ================================================================
        # 1. PROJEKTOVÉ ROLE A OPRÁVNĚNÍ
        # ================================================================
        self.stdout.write(self.style.SUCCESS('📁 Projektové role a oprávnění'))
        self.stdout.write('-' * 60)

        # Definice projektových oprávnění
        project_permissions_data = [
            ('can_view_project', 'Prohlížení projektu'),
            ('can_edit_project', 'Úprava projektu'),
            ('can_delete_project', 'Smazání projektu'),
            ('can_manage_users', 'Správa uživatelů projektu'),
            ('can_manage_settings', 'Správa nastavení projektu'),
            ('can_manage_budget', 'Správa rozpočtu'),
            ('can_create_tasks', 'Vytváření úkolů'),
            ('can_edit_tasks', 'Úprava úkolů'),
            ('can_delete_tasks', 'Mazání úkolů'),
            ('can_assign_tasks', 'Přiřazování úkolů'),
            ('can_create_documents', 'Vytváření dokumentů'),
            ('can_edit_documents', 'Úprava dokumentů'),
            ('can_delete_documents', 'Mazání dokumentů'),
            ('can_create_milestones', 'Vytváření milníků'),
            ('can_edit_milestones', 'Úprava milníků'),
            ('can_delete_milestones', 'Mazání milníků'),
            ('can_view_reports', 'Prohlížení reportů'),
            ('can_create_reports', 'Vytváření reportů'),
        ]

        # Vytvořit projektová oprávnění
        project_permissions = {}
        for perm_name, perm_desc in project_permissions_data:
            perm, created = ProjectPermission.objects.get_or_create(
                permission_name=perm_name,
                defaults={'description': perm_desc}
            )
            project_permissions[perm_name] = perm
            if created:
                self.stdout.write(f'  ✅ Vytvořeno oprávnění: {perm_name}')

        # Definice projektových rolí s jejich oprávněními
        project_roles_data = {
            'project_owner': {
                'description': 'Vlastník projektu - plná kontrola',
                'permissions': [
                    'can_view_project', 'can_edit_project', 'can_delete_project',
                    'can_manage_users', 'can_manage_settings', 'can_manage_budget',
                    'can_create_tasks', 'can_edit_tasks', 'can_delete_tasks', 'can_assign_tasks',
                    'can_create_documents', 'can_edit_documents', 'can_delete_documents',
                    'can_create_milestones', 'can_edit_milestones', 'can_delete_milestones',
                    'can_view_reports', 'can_create_reports',
                ]
            },
            'project_admin': {
                'description': 'Administrátor projektu',
                'permissions': [
                    'can_view_project', 'can_edit_project',
                    'can_manage_users', 'can_manage_settings', 'can_manage_budget',
                    'can_create_tasks', 'can_edit_tasks', 'can_delete_tasks', 'can_assign_tasks',
                    'can_create_documents', 'can_edit_documents', 'can_delete_documents',
                    'can_create_milestones', 'can_edit_milestones', 'can_delete_milestones',
                    'can_view_reports', 'can_create_reports',
                ]
            },
            'project_manager': {
                'description': 'Projektový manažer',
                'permissions': [
                    'can_view_project', 'can_edit_project',
                    'can_manage_budget',
                    'can_create_tasks', 'can_edit_tasks', 'can_assign_tasks',
                    'can_create_documents', 'can_edit_documents',
                    'can_create_milestones', 'can_edit_milestones',
                    'can_view_reports', 'can_create_reports',
                ]
            },
            'project_controller': {
                'description': 'Kontrolor projektu',
                'permissions': [
                    'can_view_project',
                    'can_manage_budget',
                    'can_view_reports', 'can_create_reports',
                ]
            },
            'project_editor': {
                'description': 'Editor projektu',
                'permissions': [
                    'can_view_project', 'can_edit_project',
                    'can_create_tasks', 'can_edit_tasks',
                    'can_create_documents', 'can_edit_documents',
                    'can_create_milestones', 'can_edit_milestones',
                ]
            },
            'project_contributor': {
                'description': 'Přispěvatel',
                'permissions': [
                    'can_view_project',
                    'can_create_tasks', 'can_edit_tasks',
                    'can_create_documents',
                ]
            },
            'project_viewer': {
                'description': 'Pozorovatel',
                'permissions': [
                    'can_view_project',
                    'can_view_reports',
                ]
            },
            'project_stakeholder': {
                'description': 'Stakeholder',
                'permissions': [
                    'can_view_project',
                    'can_view_reports',
                ]
            },
        }

        # Vytvořit projektové role
        for role_name, role_data in project_roles_data.items():
            role, created = ProjectRole.objects.get_or_create(
                role_name=role_name,
                defaults={'description': role_data['description']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Vytvořena role: {role_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  🔄 Role již existuje: {role_name}'))

            # Přiřadit oprávnění k roli
            for perm_name in role_data['permissions']:
                ProjectRolePermission.objects.get_or_create(
                    role=role,
                    permission=project_permissions[perm_name]
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(project_roles_data)} projektových rolí'))
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(project_permissions_data)} projektových oprávnění'))
        self.stdout.write('')

        # ================================================================
        # 2. ORGANIZAČNÍ ROLE A OPRÁVNĚNÍ
        # ================================================================
        self.stdout.write(self.style.SUCCESS('🏢 Organizační role a oprávnění'))
        self.stdout.write('-' * 60)

        # Definice organizačních oprávnění
        org_permissions_data = [
            ('can_view_organization', 'Prohlížení organizace'),
            ('can_edit_organization', 'Úprava organizace'),
            ('can_delete_organization', 'Smazání organizace'),
            ('can_manage_members', 'Správa členů organizace'),
            ('can_create_projects', 'Vytváření projektů'),
            ('can_manage_projects', 'Správa projektů'),
            ('can_view_all_projects', 'Prohlížení všech projektů'),
            ('can_manage_billing', 'Správa fakturace'),
            ('can_manage_settings', 'Správa nastavení organizace'),
        ]

        # Vytvořit organizační oprávnění
        org_permissions = {}
        for perm_name, perm_desc in org_permissions_data:
            perm, created = OrganizationPermission.objects.get_or_create(
                permission_name=perm_name,
                defaults={'description': perm_desc}
            )
            org_permissions[perm_name] = perm
            if created:
                self.stdout.write(f'  ✅ Vytvořeno oprávnění: {perm_name}')

        # Definice organizačních rolí
        org_roles_data = {
            'organization_owner': {
                'description': 'Vlastník organizace',
                'permissions': [
                    'can_view_organization', 'can_edit_organization', 'can_delete_organization',
                    'can_manage_members', 'can_create_projects', 'can_manage_projects',
                    'can_view_all_projects', 'can_manage_billing', 'can_manage_settings',
                ]
            },
            'organization_admin': {
                'description': 'Administrátor organizace',
                'permissions': [
                    'can_view_organization', 'can_edit_organization',
                    'can_manage_members', 'can_create_projects', 'can_manage_projects',
                    'can_view_all_projects', 'can_manage_settings',
                ]
            },
            'organization_member': {
                'description': 'Člen organizace',
                'permissions': [
                    'can_view_organization',
                    'can_create_projects',
                    'can_view_all_projects',
                ]
            },
            'organization_viewer': {
                'description': 'Pozorovatel organizace',
                'permissions': [
                    'can_view_organization',
                    'can_view_all_projects',
                ]
            },
        }

        # Vytvořit organizační role
        for role_name, role_data in org_roles_data.items():
            role, created = OrganizationRole.objects.get_or_create(
                role_name=role_name,
                defaults={'description': role_data['description']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Vytvořena role: {role_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  🔄 Role již existuje: {role_name}'))

            # Přiřadit oprávnění k roli
            for perm_name in role_data['permissions']:
                OrganizationRolePermission.objects.get_or_create(
                    role=role,
                    permission=org_permissions[perm_name]
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(org_roles_data)} organizačních rolí'))
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(org_permissions_data)} organizačních oprávnění'))
        self.stdout.write('')

        # ================================================================
        # 3. MODULOVÉ ROLE A OPRÁVNĚNÍ
        # ================================================================
        self.stdout.write(self.style.SUCCESS('🔧 Modulové role a oprávnění'))
        self.stdout.write('-' * 60)

        # Definice modulových oprávnění
        module_permissions_data = [
            ('can_read', 'Čtení dat modulu'),
            ('can_write', 'Zápis dat do modulu'),
            ('can_delete', 'Mazání dat v modulu'),
            ('can_manage', 'Správa modulu'),
        ]

        # Vytvořit modulová oprávnění
        module_permissions = {}
        for perm_name, perm_desc in module_permissions_data:
            perm, created = ModulePermission.objects.get_or_create(
                permission_name=perm_name,
                defaults={'description': perm_desc}
            )
            module_permissions[perm_name] = perm
            if created:
                self.stdout.write(f'  ✅ Vytvořeno oprávnění: {perm_name}')

        # Definice modulových rolí
        module_roles_data = {
            'module_manager': {
                'description': 'Správce modulu - plný přístup',
                'permissions': ['can_read', 'can_write', 'can_delete', 'can_manage']
            },
            'module_editor': {
                'description': 'Editor modulu - čtení, zápis, mazání',
                'permissions': ['can_read', 'can_write', 'can_delete']
            },
            'module_contributor': {
                'description': 'Přispěvatel modulu - čtení a zápis',
                'permissions': ['can_read', 'can_write']
            },
            'module_viewer': {
                'description': 'Pozorovatel modulu - pouze čtení',
                'permissions': ['can_read']
            },
        }

        # Vytvořit modulové role
        for role_name, role_data in module_roles_data.items():
            role, created = ModuleRole.objects.get_or_create(
                role_name=role_name,
                defaults={'description': role_data['description']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Vytvořena role: {role_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  🔄 Role již existuje: {role_name}'))

            # Přiřadit oprávnění k roli
            for perm_name in role_data['permissions']:
                ModuleRolePermission.objects.get_or_create(
                    role=role,
                    permission=module_permissions[perm_name]
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(module_roles_data)} modulových rolí'))
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(module_permissions_data)} modulových oprávnění'))
        self.stdout.write('')

        # ================================================================
        # SHRNUTÍ
        # ================================================================
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('✅ INICIALIZACE DOKONČENA'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'📁 Projektové: {len(project_roles_data)} rolí, {len(project_permissions_data)} oprávnění'))
        self.stdout.write(self.style.SUCCESS(f'🏢 Organizační: {len(org_roles_data)} rolí, {len(org_permissions_data)} oprávnění'))
        self.stdout.write(self.style.SUCCESS(f'🔧 Modulové: {len(module_roles_data)} rolí, {len(module_permissions_data)} oprávnění'))
        self.stdout.write(self.style.SUCCESS('='*60))
