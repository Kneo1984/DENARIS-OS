import os, sqlite3, glob
base = r'.\\data'
for p in glob.glob(os.path.join(base, '*.db')):
    try:
        con = sqlite3.connect(p); con.execute('PRAGMA schema_version;'); con.close()
        print('OK   ', os.path.basename(p))
    except Exception as e:
        print('BROKE', os.path.basename(p), '-', e)
