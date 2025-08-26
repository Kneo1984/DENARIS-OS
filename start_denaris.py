import tkinter as tk
from datetime import datetime

# === DENARIS-OS: Startmodul ===

def start_system():
    log_message("System gestartet - Self-Heal aktiv - QuantumShield geladen.")

def log_message(msg):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    text_area.insert(tk.END, f"[{timestamp}] {msg}\n")
    text_area.see(tk.END)

# --- GUI-Fenster ---
root = tk.Tk()
root.title("DENARIS-OS")
root.geometry("600x400")

# Titel-Label
title = tk.Label(root, text="DENARIS-OS", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Textbereich für Logs
text_area = tk.Text(root, wrap="word", height=15, width=70)
text_area.pack(padx=10, pady=10)

# Start-Button
start_button = tk.Button(root, text="System starten", command=start_system, bg="green", fg="white")
start_button.pack(pady=5)

# Exit-Button
exit_button = tk.Button(root, text="Beenden", command=root.quit, bg="red", fg="white")
exit_button.pack(pady=5)

# --- Start ---
log_message("DENARIS-OS Initialisiert ... bereit.")
root.mainloop()
