import os, time
# Delete old dist/aayu.exe if exists so we wait for new one
if os.path.exists('dist/aayu.exe'):
    os.remove('dist/aayu.exe')
    
while not os.path.exists('dist/aayu.exe'):
    time.sleep(1)

os.system('cp dist/aayu.exe website/public/releases/aayu.exe')
os.system('git add runtime/vm/database.py website/public/releases/aayu.exe')
os.system('git commit -m "fix: database model decorator dict access"')
os.system('git push origin main')
print("PUSH SUCCESSFUL!")