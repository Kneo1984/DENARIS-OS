import time
def boot_sequence():
    print("Initialisiere DENARIS OS Kernel...")
    for svc in ["Netzwerk","Speicher","Sicherheit","Benutzerkontrolle"]:
        print(f"Starte Dienst: {svc}")
        time.sleep(0.2)
    print("Systemdienste aktiv.")
