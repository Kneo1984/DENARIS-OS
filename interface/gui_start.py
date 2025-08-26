# ==========================================
# DENARIS OS  Visuelle Oberfläche mit Logo
# ==========================================

import tkinter as tk
from PIL import Image, ImageTk  # Bildverarbeitung

def start_gui():
    root = tk.Tk()
    root.title("DENARIS OS  Kontrollzentrum")
    root.geometry("600x400")
    root.configure(bg="#1e1e1e")

    # Logo laden
    try:
        image_path = "interface/logo.png"  # relativer Pfad
        img = Image.open(image_path)
        img = img.resize((100, 100))  # Größe anpassen
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo, bg="#1e1e1e")
        logo_label.image = logo  # Referenz speichern
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"[WARNUNG] Logo konnte nicht geladen werden: {e}")

    # Begrüßungstext
    label = tk.Label(root, text=" Willkommen in der visuellen Oberfläche von DENARIS OS",
                     font=("Arial", 14), fg="white", bg="#1e1e1e")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
