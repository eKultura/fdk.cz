# fdk_cz/management/commands/init_roles.py

from django.core.management.base import BaseCommand
from fdk_cz.models import ProjectRole, ProjectPermission, ProjectRolePermission

class Command(BaseCommand):
    help = 'Inicializovat projektové role a oprávnění'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🔐 Inicializace rolí a oprávnění...'))

        # Definice oprávnění
        permissions_data = [
            'can_view_project',
            'can_edit_project',
            'can_delete_project',
            'can_manage_users',
            'can_create_tasks',
            'can_edit_tasks',
            'can_delete_tasks',
            'can_create_documents',
            'can_delete_documents',
            'can_create_milestones',
            'can_edit_milestones',
        ]

        # Vytvořit oprávnění
        permissions = {}
        for perm_name in permissions_data:
            perm, created = ProjectPermission.objects.get_or_create(
                permission_name=perm_name
            )
            permissions[perm_name] = perm
            if created:
                self.stdout.write(f'  ✅ Vytvořeno oprávnění: {perm_name}')

        # Definice rolí s jejich oprávněními
        roles_data = {
            'Administrator': [
                'can_view_project',
                'can_edit_project',
                'can_delete_project',
                'can_manage_users',
                'can_create_tasks',
                'can_edit_tasks',
                'can_delete_tasks',
                'can_create_documents',
                'can_delete_documents',
                'can_create_milestones',
                'can_edit_milestones',
            ],
            'Manager': [
                'can_view_project',
                'can_edit_project',
                'can_create_tasks',
                'can_edit_tasks',
                'can_create_documents',
                'can_create_milestones',
                'can_edit_milestones',
            ],
            'Developer': [
                'can_view_project',
                'can_create_tasks',
                'can_edit_tasks',
                'can_create_documents',
            ],
            'Viewer': [
                'can_view_project',
            ],
        }

        # Vytvořit role
        for role_name, perm_names in roles_data.items():
            role, created = ProjectRole.objects.get_or_create(
                role_name=role_name
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Vytvořena role: {role_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  🔄 Role již existuje: {role_name}'))

            # Přiřadit oprávnění k roli
            for perm_name in perm_names:
                ProjectRolePermission.objects.get_or_create(
                    role=role,
                    permission=permissions[perm_name]
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(roles_data)} rolí'))
        self.stdout.write(self.style.SUCCESS(f'✅ Vytvořeno {len(permissions_data)} oprávnění'))
        self.stdout.write(self.style.SUCCESS('='*60))
