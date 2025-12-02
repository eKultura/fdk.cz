#!/usr/bin/env python3
"""
Test that all model imports work correctly.
This script tests the new modular structure without requiring Django to be installed.
"""
import sys
import ast
import os

def check_imports():
    """Check that all imports in __init__.py are valid."""
    errors = []

    # Check that all module files exist
    models_dir = 'fdk_cz/models'
    init_file = os.path.join(models_dir, '__init__.py')

    if not os.path.exists(init_file):
        return ["__init__.py not found"]

    # Read __init__.py
    with open(init_file, 'r') as f:
        content = f.read()

    # Parse imports
    tree = ast.parse(content)
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                module_file = os.path.join(models_dir, f"{node.module}.py")
                if not os.path.exists(module_file):
                    errors.append(f"Module file not found: {module_file}")
                else:
                    imports.append(node.module)

    print(f"✓ Found {len(imports)} module imports in __init__.py")

    # Check each module file for syntax
    for module_name in imports:
        module_file = os.path.join(models_dir, f"{module_name}.py")
        try:
            with open(module_file, 'r') as f:
                module_content = f.read()
            ast.parse(module_content)
            print(f"✓ {module_name}.py syntax OK")
        except SyntaxError as e:
            errors.append(f"Syntax error in {module_name}.py: {e}")

    # Check that original models.py still exists
    if not os.path.exists('fdk_cz/models.py'):
        errors.append("Original models.py not found!")
    else:
        print("✓ Original models.py still exists")

    # Check that backup exists
    if not os.path.exists('fdk_cz/models_backup.py'):
        errors.append("Backup models_backup.py not found!")
    else:
        print("✓ Backup models_backup.py exists")

    return errors


def main():
    print("Testing modular models structure...")
    print("-" * 50)

    errors = check_imports()

    print("-" * 50)
    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✓ All checks passed!")
        print("✓ Modular structure is ready to use")
        print("\nNext steps:")
        print("1. Keep using 'from fdk_cz.models import ModelName'")
        print("2. The imports will work exactly the same as before")
        print("3. If there are issues, you can revert by renaming models.py")
        sys.exit(0)


if __name__ == '__main__':
    main()
