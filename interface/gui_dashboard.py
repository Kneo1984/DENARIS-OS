# ==========================================
# DENARIS OS – Grafisches Kontrollzentrum
# Datei: interface/gui_dashboard.py
# Autor: Dennis Maier (KNEO1984)
# Zweck: Dashboard mit Logo, Status, NetWatch, Logs, Diagnose, Exit
# ==========================================

from __future__ import annotations

import os
import sys
import json
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

# Projektwurzel sicherstellen
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# optionale Abhängigkeiten
try:
    from PIL import Image, ImageTk  # pip install pillow
    PIL_AVAILABLE = True
except Exception as e:
    PIL_AVAILABLE = False
    Image = ImageTk = None
    print(f"[WARNUNG] Pillow/PIL nicht verfügbar: {e}")

try:
    import psutil  # pip install psutil
    PSUTIL_AVAILABLE = True
except Exception as e:
    PSUTIL_AVAILABLE = False
    print(f"[WARNUNG] psutil nicht verfügbar: {e}")

try:
    from utils import net_watch
    NETWATCH_AVAILABLE = True
except Exception as e:
    NETWATCH_AVAILABLE = False
    net_watch = None
    print(f"[WARNUNG] NetWatch-Modul nicht verfügbar: {e}")


class DenarisDashboard(tk.Tk):
    def __init__(self, config: dict | None = None):
        super().__init__()
        self.title("DENARIS OS – Kontrollzentrum")
        self.geometry("980x640")
        self.minsize(820, 520)
        self.configure(bg="#0f141a")

        self.config_dict = config or self._load_config()
        self.netwatch_obj = None
        self.netwatch_running = False

        self._build_header()
        self._build_toolbar()
        self._build_status_area()
        self._build_footer()

        self._update_status("System bereit.", ok=True)

        # optionaler Autostart von NetWatch
        if self.config_dict.get("enable_net_watch") in (True, "true", "True"):
            self.after(300, self._start_netwatch)

    # --- Config laden ---
    def _load_config(self) -> dict:
        cfg_path = os.path.join(PROJECT_ROOT, "data", "settings.json")
        try:
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"[WARNUNG] Konnte settings.json nicht lesen: {e}")
        return {
            "enable_net_watch": True,
            "net_watch": {"interval": 5, "limit": 200, "alert_on_new": True},
        }

    # --- Header ---
    def _build_header(self):
        header = tk.Frame(self, bg="#0f141a")
        header.pack(fill="x", pady=(18, 10))

        logo_candidate_paths = [
            os.path.join(PROJECT_ROOT, "interface", "logo.png"),
            os.path.join(PROJECT_ROOT, "DENARIS_OS_LOGO.png"),
        ]
        if PIL_AVAILABLE:
            for p in logo_candidate_paths:
                if os.path.exists(p):
                    try:
                        img = Image.open(p)
                        img.thumbnail((220, 220), Image.LANCZOS)
                        logo = ImageTk.PhotoImage(img)
                        lbl = tk.Label(header, image=logo, bg="#0f141a")
                        lbl.image = logo
                        lbl.pack(pady=(0, 6))
                        break
                    except Exception as e:
                        print(f"[WARNUNG] Logo konnte nicht geladen werden ({p}): {e}")

        tk.Label(
            header, text="DENARIS  OS",
            fg="#cfe8ff", bg="#0f141a", font=("Segoe UI", 30, "bold")
        ).pack()
        tk.Label(
            header,
            text="Visuelles Kontrollzentrum • Schutz • Transparenz • Souveränität",
            fg="#8fb3d9", bg="#0f141a", font=("Segoe UI", 12)
        ).pack(pady=(4, 0))

    # --- Toolbar ---
    def _build_toolbar(self):
        bar = tk.Frame(self, bg="#0c1117")
        bar.pack(fill="x", padx=14, pady=14)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Denaris.TButton", font=("Segoe UI", 10, "bold"), padding=8)

        self.btn_start = ttk.Button(
            bar, text="Netzwerküberwachung START",
            style="Denaris.TButton", command=self._start_netwatch
        )
        self.btn_stop = ttk.Button(
            bar, text="Netzwerküberwachung STOP",
            style="Denaris.TButton", command=self._stop_netwatch, state="disabled"
        )
        self.btn_logs = ttk.Button(
            bar, text="Logs öffnen", style="Denaris.TButton", command=self._open_logs
        )
        self.btn_diag = ttk.Button(
            bar, text="Systemdiagnose", style="Denaris.TButton", command=self._run_diagnose
        )
        self.btn_about = ttk.Button(
            bar, text="Über DENARIS", style="Denaris.TButton", command=self._show_about
        )
        self.btn_clear = ttk.Button(
            bar, text="Ausgabe leeren", style="Denaris.TButton",
            command=lambda: self.output.delete("1.0", "end")
        )
        self.btn_exit = ttk.Button(
            bar, text="Beenden", style="Denaris.TButton", command=self._graceful_exit
        )

        for w in (self.btn_start, self.btn_stop, self.btn_logs, self.btn_diag, self.btn_about, self.btn_clear):
            w.pack(side="left", padx=(6, 8))
        self.btn_exit.pack(side="right", padx=(8, 6))

    # --- Statusbereich ---
    def _build_status_area(self):
        wrap = tk.Frame(self, bg="#0f141a")
        wrap.pack(fill="both", expand=True, padx=14)

        self.status_label = tk.Label(
            wrap, text="Status: –", fg="#bcd0db", bg="#0f141a",
            font=("Segoe UI", 12, "bold"), anchor="w"
        )
        self.status_label.pack(fill="x", pady=(0, 6))

        self.output = ScrolledText(
            wrap, height=18, bg="#0b1117", fg="#d7e3f1",
            insertbackground="#d7e3f1", relief="flat", wrap="word"
        )
        self.output.configure(font=("Consolas", 10))
        self.output.pack(fill="both", expand=True)

        self._ui_log(
            "Willkommen im DENARIS Kontrollzentrum.\n"
            "• START: NetWatch im Hintergrund aktivieren\n"
            "• LOGS ÖFFNEN: System-Logs einsehen\n"
            "• SYSTEMDIAGNOSE: CPU/RAM/Prozesse prüfen\n"
        )

    # --- Footer ---
    def _build_footer(self):
        footer = tk.Frame(self, bg="#0f141a")
        footer.pack(fill="x", pady=(6, 12))
        tk.Label(
            footer, text="© Dennis Maier – DENARIS OS",
            fg="#5f7889", bg="#0f141a", font=("Segoe UI", 9)
        ).pack()

    # --- Aktionen ---
    def _start_netwatch(self):
        if self.netwatch_running:
            self._update_status("NetWatch läuft bereits.", ok=True)
            return
        if not NETWATCH_AVAILABLE:
            self._update_status("NetWatch-Modul nicht verfügbar.", ok=False)
            return

        cfg = self.config_dict.get("net_watch", {})
        self._ui_log("Starte NetWatch …")

        def _run():
            try:
                self.netwatch_obj = net_watch.start_monitor_in_background(
                    config=cfg, alert_callback=self._alert_from_thread
                )
                self.netwatch_running = True
                self._update_status("NetWatch aktiv.", ok=True)
                self.btn_start.configure(state="disabled")
                self.btn_stop.configure(state="normal")
            except Exception as e:
                self._update_status(f"Fehler beim Starten von NetWatch: {e}", ok=False)

        threading.Thread(target=_run, daemon=True).start()

    def _stop_netwatch(self):
        if not self.netwatch_running or not self.netwatch_obj:
            self._update_status("NetWatch war nicht aktiv.", ok=True)
            return
        try:
            self.netwatch_obj.stop()
        except Exception:
            pass
        self.netwatch_obj = None
        self.netwatch_running = False
        self._update_status("NetWatch gestoppt.", ok=True)
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")

    def _run_diagnose(self):
        if not PSUTIL_AVAILABLE:
            self._update_status("psutil nicht installiert – Diagnose nicht verfügbar.", ok=False)
            return

        def _work():
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            procs = len(psutil.pids())
            self._safe_ui_log(f"[DIAGNOSE] CPU: {cpu:.0f}% | RAM: {ram:.0f}% | Prozesse: {procs}")

        threading.Thread(target=_work, daemon=True).start()

    def _open_logs(self):
        logs_dir = os.path.join(PROJECT_ROOT, "logs")
        if os.path.isdir(logs_dir):
            try:
                if sys.platform.startswith("win"):
                    os.startfile(logs_dir)  # type: ignore[attr-defined]
                elif sys.platform == "darwin":
                    os.system(f"open '{logs_dir}'")
                else:
                    os.system(f"xdg-open '{logs_dir}'")
                self._update_status("Logs geöffnet.", ok=True)
            except Exception as e:
                self._update_status(f"Logs konnten nicht geöffnet werden: {e}", ok=False)
        else:
            self._update_status("Log-Verzeichnis nicht gefunden.", ok=False)

    def _show_about(self):
        messagebox.showinfo(
            "Über DENARIS",
            "DENARIS OS – Ethisches Kontrollsystem für digitale Souveränität.\n"
            "Autor: Dennis Maier (KNEO1984)\n"
            "Schutz • Transparenz • Freiheit"
        )

    def _graceful_exit(self):
        if self.netwatch_running and self.netwatch_obj:
            try:
                self.netwatch_obj.stop()
            except Exception:
                pass
        self.destroy()

    # --- Thread-sichere UI-Helfer ---
    def _ui_log(self, text: str):
        if not text.endswith("\n"):
            text += "\n"
        self.output.insert("end", text)
        self.output.see("end")

    def _safe_ui_log(self, text: str):
        self.after(0, self._ui_log, text)

    def _alert_from_thread(self, msg: str):
        self._safe_ui_log(f"[ALERT] {msg}")

    def _update_status(self, text: str, ok: bool = True):
        self.status_label.configure(text=f"Status: {text}", fg=("#9fe870" if ok else "#ff7d7d"))


def start_gui(config: dict | None = None):
    app = DenarisDashboard(config=config)
    app.mainloop()


if __name__ == "__main__":
    start_gui()
