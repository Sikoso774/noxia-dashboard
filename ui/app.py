import os
import customtkinter as ctk
from PIL import Image
from config.settings import COLORS, FONTS, ASSETS_DIR, LOGO_FILENAME, LOGO_WIDTH
from ui.tab_list import TabListe
from ui.tab_supervision import TabSupervision
from ui.setup_frame import SetupFrame
from services.api_client import API_Client

from ui.setup_frame import SetupFrame
from config.settings import settings, COLORS

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NOXIA SECURITY")
        self.geometry("1200x800")
        self.configure(fg_color=COLORS["bg"])

        # Au démarrage, on vérifie la clé
        if not settings.API_KEY:
            self.show_setup()
        else:
            self.init_dashboard()

    def show_setup(self):
        """Affiche le formulaire de configuration"""
        self.setup_view = SetupFrame(self, on_success=self.complete_setup)
        self.setup_view.pack(fill="both", expand=True)

    def complete_setup(self, key):
        """Appelé quand la clé est validée"""
        settings.API_KEY = key
        self.setup_view.pack_forget() # On retire proprement le cadre de setup
        self.init_dashboard()        # On lance le vrai contenu

    def init_dashboard(self) -> None:
        """Initialise le contenu du dashboard (API, Tabs, etc.)."""
        self.api = API_Client()
        # 1. AJOUTE CES DEUX LIGNES : Création du conteneur principal
        self.container = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        # 2. Ton code existant continue ici...
        self.header = ctk.CTkFrame(self.container, fg_color="transparent")
        
        # Header
        self.header = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header.pack(pady=20, padx=20, fill="x")
        self._load_logo(self.header)

        # Tabs
        self.tabview = ctk.CTkTabview(self.container, fg_color=COLORS["bg"])
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        t1 = self.tabview.add("Liste des Liens")
        t2 = self.tabview.add("Supervision")
        
        self.tab_supervision = TabSupervision(t2, self.api)
        self.tab_liste = TabListe(t1, self.api, self.go_to_monitoring)

    def _load_logo(self, parent):
        try:
            path = os.path.join(ASSETS_DIR, LOGO_FILENAME)
            img = Image.open(path)
            logo = ctk.CTkImage(img, size=(LOGO_WIDTH, int(LOGO_WIDTH * (img.height/img.width))))
            ctk.CTkLabel(parent, image=logo, text="").pack(side="left")
        except: pass

    def go_to_monitoring(self, link):
        self.tabview.set("Supervision")
        self.tab_supervision.load_client(link)
