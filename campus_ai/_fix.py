import re, glob

def fix_file(fp):
    c = open(fp, 'r', encoding='utf-8').read()
    o = c
    c = re.sub(r'for (\w+): \w+(?:\[.*?\])? in ', r'for \1 in ', c)
    c = c.replace('except Exception as e: Exception:', 'except Exception as e:')
    c = re.sub(r'with open\(([^)]+)\) as (\w+): [^:]+:', r'with open(\1) as \2:', c)
    c = re.sub(r'(\s+)(\w+): sys\.Any \| \w+ = ', r'\1\2 = ', c)
    c = re.sub(r'(def \w+\([^)]*\))\s*-> sys\.\w+:', r'\1:', c)
    c = re.sub(r'except (\w+(?:\.\w+)*) as (\w+): \w+(?:\.\w+)*:', r'except \1 as \2:', c)
    if c != o:
        open(fp, 'w', encoding='utf-8').write(c)
        print('FIXED:', fp)

for f in glob.glob('**/*.py', recursive=True):
    if '_fix' in f:
        continue
    fix_file(f)
