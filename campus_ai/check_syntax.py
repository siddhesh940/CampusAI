import py_compile

files: list[str] = [
    'main.py', 'auth.py', 'database.py', 'models.py',
    'services/stage_service.py', 'services/reminder_service.py',
    'services/onboarding_engine.py', 'views/dashboard.py',
    'views/onboarding_chat.py', 'views/profile.py',
    'views/admin_panel.py', 'views/portals.py'
]

all_ok = True
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print("OK:", f)
    except py_compile.PyCompileError as e:
        print("FAIL:", f, "-", e)
        all_ok = False

if all_ok:
    print("\nAll files OK!")
else:
    print("\nSome files have errors!")
