"""Fix formatter corruption in all project files."""
import re
import os

fixes: dict[str, list[tuple[str, str]]] = {
    'main.py': [
        ('with open(env_path, "r") as ef:', 'with open(env_path, "r") as ef:'),
        ('for line in ef:', 'for line in ef:'),
        ('with open(css_path, "r") as f:', 'with open(css_path, "r") as f:'),
    ],
    'auth.py': [
        ('except Exception as e:', 'except Exception as e:'),
    ],
    'services/onboarding_engine.py': [
        ('with open(KB_PATH, "r", encoding="utf-8") as f:', 'with open(KB_PATH, "r", encoding="utf-8") as f:'),
        ('with open(KB_PATH, "r", encoding="utf-8") as f:', 'with open(KB_PATH, "r", encoding="utf-8") as f:'),
        ('for kw in keywords:', 'for kw in keywords:'),
        ('for kw in kw_list:', 'for kw in kw_list:'),
    ],
    'pages/admin_panel.py': [
        ('for row in branches:', 'for row in branches:'),
    ],
    'pages/portals.py': [
        ('for doc in docs:', 'for doc in docs:'),
        ('for doc in docs_required:', 'for doc in docs_required:'),
        ('for fac in facilities:', 'for fac in facilities:'),
    ],
}

# Also fix sys.Any patterns across ALL .py files
sys_any_pattern: re.Pattern[str] = re.compile(r': sys\.Any \| \w+ =')

def fix_file(filepath, specific_fixes) -> bool:
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content: str = f.read()
    
    original: str = content
    
    # Apply specific fixes
    for old, new in specific_fixes:
        content: str = content.replace(old, new)
    
    # Fix sys.Any patterns: "var: sys.Any | Type = value" -> "var = value"
    content: str = re.sub(r'(\s+)(\w+): sys\.Any \| \w+ = ', r'\1\2 = ', content)
    
    # Fix duplicate DeltaGenerator imports
    lines: list[str] = content.split('\n')
    seen_imports = set()
    new_lines = []
    for line in lines:
        stripped: str = line.strip()
        if stripped.startswith('from streamlit.delta_generator import'):
            if stripped in seen_imports:
                continue
            seen_imports.add(stripped)
        if stripped.startswith('from typing import') and stripped in seen_imports:
            continue
        if stripped.startswith('from sqlalchemy') and stripped in seen_imports:
            continue
        seen_imports.add(stripped)
        new_lines.append(line)
    content: str = '\n'.join(new_lines)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {filepath}")
        return True
    else:
        print(f"OK: {filepath} (no changes needed)")
        return False


# Fix all files with specific fixes
for filepath, file_fixes in fixes.items():
    fix_file(filepath, file_fixes)

# Fix sys.Any in ALL .py files
for root, dirs, files in os.walk('.'):
    for fname in files:
        if fname.endswith('.py') and fname != 'fix_corruption.py' and fname != 'check_syntax.py':
            fpath: str = os.path.join(root, fname)
            fix_file(fpath, [])

print("\nDone! Run check_syntax.py to verify.")
