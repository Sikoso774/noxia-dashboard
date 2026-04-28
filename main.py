import sys
import os

# # --- 🛑 FIX ANTI-CRASH (COMPILATION SANS CONSOLE) 🛑 ---
# # Si la console est désactivée (sys.stdout est None), les 'print' font crasher l'appli.
# # On redirige donc les prints et les erreurs fatales vers un fichier texte.
# if sys.stdout is None or sys.stderr is None:
#     # On crée/ouvre un fichier de log dans le dossier de l'exécutable
#     log_file = open("noxia_debug.log", "a", encoding="utf-8")
#     sys.stdout = log_file
#     sys.stderr = log_file
# # -------------------------------------------------------

import keyring
import config.settings
from config.settings import settings
from ui.app import App

if __name__ == "__main__":
    try:
        # On lance l'app, elle gérera son propre état interne
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)