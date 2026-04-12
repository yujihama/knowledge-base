import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
path = r'C:\Users\nyham\Downloads\kb-system\kb-system\scripts\process_inbox.py'
with open(path, encoding='utf-8') as f:
    content = f.read()
print(content[-1200:])
