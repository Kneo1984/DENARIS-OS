import os, logging, logging.handlers, logging
from core.init import start_core
from syscore.init_system import boot_sequence
from interface.gui_dashboard import start_gui

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=os.path.join("logs","denaris.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

boot_sequence()
start_core()
start_gui()

