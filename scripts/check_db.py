# =========================================================
# DENARIS-OS © 2025 Dennis Maier (KNEO)
# Alle Rechte vorbehalten.
# Private & nichtkommerzielle Nutzung erlaubt.
# Kommerzielle Nutzung nur mit ausdrücklicher Genehmigung.
# =========================================================
import os, sqlite3, glob
base = r'.\\data'
for p in glob.glob(os.path.join(base, '*.db')):
    try:
        con = sqlite3.connect(p); con.execute('PRAGMA schema_version;'); con.close()
        print('OK   ', os.path.basename(p))
    except Exception as e:
        print('BROKE', os.path.basename(p), '-', e)

