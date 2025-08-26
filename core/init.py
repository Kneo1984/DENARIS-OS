# =========================================================
# DENARIS-OS © 2025 Dennis Maier (KNEO)
# Alle Rechte vorbehalten.
# Private & nichtkommerzielle Nutzung erlaubt.
# Kommerzielle Nutzung nur mit ausdrücklicher Genehmigung.
# =========================================================
# ===============================================
# DENARIS OS  Kerninitialisierung
# ===============================================
import os, sys, json, logging

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def start_core():
    print("Initialisierung des Systemkerns läuft...")
    required_dirs = ["data","logs","modules","interface","utils"]
    for d in required_dirs:
        p = os.path.join(PROJECT_ROOT, d)
        os.makedirs(p, exist_ok=True)

    cfg_path = os.path.join(PROJECT_ROOT, "data", "settings.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        print("Konfiguration geladen.")
    else:
        cfg = {"mode":"default","version":"1.0","author":"Dennis Maier",
               "system_name":"DENARIS OS","security_level":"high",
               "enable_net_watch": True, "net_watch": {"interval":5}}
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        print("Standardkonfiguration erstellt.")

    try:
        if cfg.get("enable_net_watch"):
            from utils import net_watch
            nw_cfg = cfg.get("net_watch", {})
            net_watch.start_monitor_in_background(config=nw_cfg)
            print("NetWatch (Hintergrund) gestartet.")
    except Exception as e:
        logging.getLogger().exception("NetWatch konnte nicht gestartet werden: %s", e)

    print("Systemkern vollständig geladen.")

