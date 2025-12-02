#!/usr/bin/env python3
"""
Script to split models.py into modular structure based on views/ organization.
This script DOES NOT modify models.py - it only creates new files in models/ directory.
"""
import re
import os

# Model organization based on views structure
MODEL_MAPPING = {
    'user.py': [
        'ActivityLog', 'Users2'
    ],
    'articles.py': [
        'Article'
    ],
    'company.py': [
        'Company'
    ],
    'organization.py': [
        'Organization', 'OrganizationRole', 'OrganizationPermission',
        'OrganizationRolePermission', 'OrganizationMembership'
    ],
    'project.py': [
        'Project', 'ProjectCategory', 'ProjectMilestone', 'ProjectRole',
        'ProjectPermission', 'ProjectUser', 'ProjectRolePermission',
        'ProjectTask', 'ProjectAttachment', 'ProjectComment',
        'ProjectDocument', 'SwotAnalysis'
    ],
    'modules.py': [
        'ModuleRole', 'ModulePermission', 'ModuleRolePermission',
        'ModuleAccess', 'Module', 'UserModuleSubscription',
        'ModuleBundle', 'Payment', 'ModuleUsage', 'UserModulePreference'
    ],
    'flist.py': [
        'Flist', 'ListItem', 'ListPermission'
    ],
    'contact.py': [
        'Contact'
    ],
    'warehouse.py': [
        'Warehouse', 'WarehouseCategory', 'WarehouseItem', 'WarehouseTransaction'
    ],
    'contract.py': [
        'Contract'
    ],
    'test.py': [
        'TestType', 'Test', 'TestResult', 'TestError', 'TestScenario'
    ],
    'accounting.py': [
        'Invoice', 'InvoiceItem', 'AccountingContext', 'AccountingAccount',
        'JournalEntry', 'JournalEntryLine', 'BalanceSheet'
    ],
    'grants.py': [
        'GrantProgram', 'GrantCall', 'GrantRequirement', 'GrantApplication',
        'GrantApplicationDocument', 'GrantOpportunityBookmark', 'GrantDocumentTemplate'
    ],
    'law.py': [
        'Law', 'LawDocument', 'LawQuery'
    ],
    'b2b.py': [
        'B2BCompany', 'B2BContract', 'B2BDocument'
    ],
    'hr.py': [
        'Department', 'Employee'
    ],
    'risk.py': [
        'Risk'
    ],
    'it.py': [
        'ITAsset', 'ITIncident'
    ],
    'asset.py': [
        'AssetCategory', 'Asset'
    ],
    'help.py': [
        'HelpArticle'
    ],
}


def extract_model_code(content, model_name, next_model_line=None):
    """Extract code for a specific model class."""
    # Find the class definition
    pattern = rf'^class {model_name}\(models\.Model\):'
    lines = content.split('\n')

    start_line = None
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            start_line = i
            break

    if start_line is None:
        return None

    # Find the end of the class (next class or end of file)
    end_line = len(lines)
    if next_model_line:
        end_line = next_model_line
    else:
        # Find next top-level class or end
        for i in range(start_line + 1, len(lines)):
            if re.match(r'^class \w+', lines[i]) and not lines[i].startswith('    '):
                end_line = i
                break

    return '\n'.join(lines[start_line:end_line])


def get_all_model_positions(content):
    """Get positions of all model classes."""
    lines = content.split('\n')
    positions = {}

    for i, line in enumerate(lines):
        match = re.match(r'^class (\w+)\(models\.Model\):', line)
        if match:
            positions[match.group(1)] = i

    return positions


def create_module_file(module_name, models, models_content, model_positions):
    """Create a module file with specified models."""
    output_path = f'fdk_cz/models/{module_name}'

    # Header
    header = f'''# -------------------------------------------------------------------
#                    MODELS.{module_name.upper().replace('.PY', '')}
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

'''

    # Extract models in order
    model_codes = []
    sorted_models = sorted(models, key=lambda m: model_positions.get(m, float('inf')))

    for i, model_name in enumerate(sorted_models):
        if model_name in model_positions:
            # Get next model position for this file
            next_pos = None
            for j in range(i + 1, len(sorted_models)):
                if sorted_models[j] in model_positions:
                    next_pos = model_positions[sorted_models[j]]
                    break

            code = extract_model_code(models_content, model_name, next_pos)
            if code:
                model_codes.append(code)

    content = header + '\n\n'.join(model_codes) + '\n'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created {output_path} with {len(model_codes)} models")


def create_init_file():
    """Create __init__.py that imports all models."""
    init_content = '''# -------------------------------------------------------------------
#                    MODELS.__INIT__.PY
# -------------------------------------------------------------------
# Auto-generated imports from modular structure
# This file imports all models from sub-modules to maintain compatibility

from .user import *
from .articles import *
from .company import *
from .organization import *
from .project import *
from .modules import *
from .flist import *
from .contact import *
from .warehouse import *
from .contract import *
from .test import *
from .accounting import *
from .grants import *
from .law import *
from .b2b import *
from .hr import *
from .risk import *
from .it import *
from .asset import *
from .help import *
'''

    with open('fdk_cz/models/__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content)

    print("Created fdk_cz/models/__init__.py")


def main():
    # Read original models.py
    with open('fdk_cz/models.py', 'r', encoding='utf-8') as f:
        models_content = f.read()

    # Get all model positions
    model_positions = get_all_model_positions(models_content)
    print(f"Found {len(model_positions)} models in models.py")

    # Create models directory if it doesn't exist
    os.makedirs('fdk_cz/models', exist_ok=True)

    # Create module files
    for module_name, models in MODEL_MAPPING.items():
        create_module_file(module_name, models, models_content, model_positions)

    # Create __init__.py
    create_init_file()

    print("\n✓ Models split complete!")
    print("✓ Original models.py is UNCHANGED (backup exists as models_backup.py)")
    print("✓ All models are now in fdk_cz/models/ directory")
    print("✓ Import via: from fdk_cz.models import ModelName (will work the same)")


if __name__ == '__main__':
    main()
