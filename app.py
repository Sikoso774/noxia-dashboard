import os
import requests
import customtkinter as ctk
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION IDENTITÉ VISUELLE NOXIA ---
COLOR_PRIMARY = "#1f538d"
COLOR_SECONDARY = "#2b2b2b"
COLOR_ACCENT = "#2ecc71"
COLOR_BG = "#121212"

BASE_URL = "https://kissapi.kissgroup.io/kisslink"
API_KEY = os.getenv("KISSGROUP_API_KEY")

class NoxiaDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Noxia Security - Dashboard")
        self.geometry("950x750")
        self.configure(fg_color=COLOR_BG)

        # Stockage pour la recherche locale
        self.all_links = []

        # --- HEADER AVEC LOGO (Ton calcul de ratio) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20, padx=20, fill="x")

        try:
            basedir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(basedir, "logo-noxia.png") 
            pil_img = Image.open(logo_path)
            
            width_wanted = 400
            ratio = pil_img.height / pil_img.width
            height_calculated = int(width_wanted * ratio)
            
            logo_img = ctk.CTkImage(light_image=pil_img,
                                    dark_image=pil_img,
                                    size=(width_wanted, height_calculated))
            
            self.logo_label = ctk.CTkLabel(self.header_frame, image=logo_img, text="")
            self.logo_label.pack(side="left", padx=(0, 20))
        except Exception as e:
            print(f"Erreur chargement logo : {e}")

        # --- ONGLETS ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=COLOR_PRIMARY)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.tab_liste = self.tabview.add("Liste des Liens")
        self.tab_supervision = self.tabview.add("Supervision")

        self.setup_tab_liste()
        self.setup_tab_supervision()

    # ==========================================
    # ONGLET 1 : INVENTAIRE ET RECHERCHE
    # ==========================================
    def setup_tab_liste(self):
        # Barre de recherche (Frame)
        self.search_frame = ctk.CTkFrame(self.tab_liste, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(self.search_frame, 
                                         placeholder_text="Rechercher un client, une ville ou un code...", 
                                         width=450, height=35)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_links)

        self.btn_load = ctk.CTkButton(self.search_frame, text="CHARGER API", command=self.load_links)
        self.btn_load.pack(side="right")

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_liste, fg_color="transparent")
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def load_links(self):
        """Récupère les liens via l'API """
        headers = {"api_key": API_KEY}
        try:
            response = requests.get(f"{BASE_URL}/links", headers=headers)
            response.raise_for_status()
            self.all_links = response.json()
            self.display_links(self.all_links)
        except Exception as e:
            self.show_message(f"Erreur : {e}")

    def display_links(self, links_to_show):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for link in links_to_show:
            card = ctk.CTkFrame(self.scroll_frame, fg_color=COLOR_SECONDARY, border_width=1, border_color="#3d3d3d")
            card.pack(fill="x", padx=10, pady=5)

            info = f"{link.get('client_name')}\n{link.get('link_code')} | {link.get('techno_name')}"
            ctk.CTkLabel(card, text=info, font=("Arial", 13, "bold"), justify="left").pack(side="left", padx=15, pady=10)

            # Bouton pour basculer et superviser
            ctk.CTkButton(card, text="SUPERVISER", width=100, 
                          command=lambda l=link: self.go_to_monitoring(l)).pack(side="right", padx=15)

    def filter_links(self, event=None):
        query = self.search_entry.get().lower()
        filtered = [l for l in self.all_links if query in str(l).lower()]
        self.display_links(filtered)

    def go_to_monitoring(self, link):
        self.tabview.set("Supervision")
        self.label_client.configure(text=f"Client : {link.get('client_name')}")
        self.label_address.configure(text=f"Adresse : {link.get('address')}")
        self.fetch_monitoring_data()

    def show_message(self, msg):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.scroll_frame, text=msg).pack(pady=20)

    # ==========================================
    # ONGLET 2 : SUPERVISION
    # ==========================================
    def setup_tab_supervision(self):
        self.label_client = ctk.CTkLabel(self.tab_supervision, text="Sélectionnez un lien dans la liste.", font=("Arial", 14))
        self.label_client.pack(pady=(40, 10))

        self.label_address = ctk.CTkLabel(self.tab_supervision, text="", font=("Arial", 12))
        self.label_address.pack(pady=10)

        self.label_status = ctk.CTkLabel(self.tab_supervision, text="-", font=("Arial", 25, "bold"))
        self.label_status.pack(pady=30)

        self.btn_mon = ctk.CTkButton(self.tab_supervision, text="Rafraîchir Statut", command=self.fetch_monitoring_data)
        self.btn_mon.pack(pady=20)

    def fetch_monitoring_data(self):
        """Utilise l'endpoint monitoring testé avec succès """
        headers = {"api_key": API_KEY}
        try:
            response = requests.get(f"{BASE_URL}/monitoring", headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Gestion du format (liste ou objet unique) 
            lien = data[0] if isinstance(data, list) else data
            
            status = str(lien.get('status_display', 'inconnu')).lower()
            color = COLOR_ACCENT if status == 'ok' else "#e74c3c"
            self.label_status.configure(text=f"STATUT : {status.upper()}", text_color=color)
        except Exception as e:
            self.label_status.configure(text="Erreur Supervision", text_color="red")

if __name__ == "__main__":
    app = NoxiaDashboard()
    app.mainloop()