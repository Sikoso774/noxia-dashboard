import os
import csv
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

# Import de nos propres modules
import config
from api_client import API_Client

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Noxia Security - Dashboard")
        self.geometry("1000x800")
        self.configure(fg_color=config.COLORS["bg"])

        # Initialisation du client API
        self.api = API_Client(config.BASE_URL, config.API_KEY)
        self.all_links = [] # Cache pour l'export et la recherche

        # --- HEADER AVEC LOGO ---
        self.setup_header()

        # --- ONGLETS ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=config.COLORS["primary"])
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.tab_liste = self.tabview.add("Liste des Liens")
        self.tab_supervision = self.tabview.add("Supervision")

        # Initialisation de l'interface
        self.setup_tab_liste()
        self.setup_tab_supervision()
        self.auto_refresh_monitoring()

    def setup_header(self):
        """Configure le bandeau supérieur avec le logo Noxia"""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20, padx=20, fill="x")

        try:
            basedir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(basedir, config.LOGO_FILENAME) 
            pil_img = Image.open(logo_path)
            
            ratio = pil_img.height / pil_img.width
            height_calculated = int(config.LOGO_WIDTH * ratio)
            
            logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(config.LOGO_WIDTH, height_calculated))
            self.logo_label = ctk.CTkLabel(self.header_frame, image=logo_img, text="")
            self.logo_label.pack(side="left", padx=(0, 20))
        except Exception as e:
            print(f"Erreur logo : {e}")

    # ==========================================
    # ONGLET 1 : LISTE DES LIENS
    # ==========================================
    def setup_tab_liste(self):
        # Frame de contrôle (Recherche + Boutons)
        self.ctrl_frame = ctk.CTkFrame(self.tab_liste, fg_color="transparent")
        self.ctrl_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(self.ctrl_frame, placeholder_text="Rechercher...", width=350, height=35)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_links)

        # Bouton Charger
        self.btn_load = ctk.CTkButton(self.ctrl_frame, text="CHARGER API", fg_color=config.COLORS["primary"], command=self.load_links)
        self.btn_load.pack(side="left", padx=5)

        # Bouton Exporter CSV
        self.btn_export = ctk.CTkButton(self.ctrl_frame, text="EXPORTER CSV", fg_color="#27ae60", hover_color="#1e8449", command=self.export_to_csv)
        self.btn_export.pack(side="left", padx=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_liste, fg_color="transparent")
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def load_links(self):
        """Utilise l'API_Client pour récupérer les liens [cite: 1]"""
        try:
            self.all_links = self.api.get_links()
            self.display_links(self.all_links)
        except Exception as e:
            self.show_message(f"Erreur : {e}")

    def display_links(self, links_to_show):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        for link in links_to_show:
            card = ctk.CTkFrame(self.scroll_frame, fg_color=config.COLORS["card"], border_width=1, border_color=config.COLORS["border"])
            card.pack(fill="x", padx=10, pady=5)

            info = f"{link.get('client_name')}\n{link.get('link_code')} | {link.get('techno_name')}"
            ctk.CTkLabel(card, text=info, font=("Arial", 13, "bold"), justify="left").pack(side="left", padx=15, pady=10)

            status = link.get('status_admin')
            color = config.COLORS["accent"] if status == "Livré" else "#f1c40f"
            ctk.CTkLabel(card, text=f"● {status}", text_color=color).pack(side="left", padx=20)

            ctk.CTkButton(card, text="SUPERVISER", width=100, fg_color=config.COLORS["primary"],
                          command=lambda l=link: self.go_to_monitoring(l)).pack(side="right", padx=15)

    def filter_links(self, event=None):
        query = self.search_entry.get().lower()
        filtered = [l for l in self.all_links if query in str(l).lower()]
        self.display_links(filtered)

    def export_to_csv(self):
        """Exporte l'inventaire actuel en fichier CSV"""
        if not self.all_links:
            messagebox.showwarning("Export Impossible", "Veuillez d'abord charger la liste des liens.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")],
            title="Enregistrer l'inventaire Noxia",
            initialfile="inventaire_noxia.csv"
        )

        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(["Client", "Code Lien", "Adresse", "Techno", "Débit", "Statut Admin", "Référence Partenaire"])
                    
                    for link in self.all_links:
                        writer.writerow([
                            link.get('client_name'),
                            link.get('link_code'),
                            link.get('address'),
                            link.get('techno_name'),
                            link.get('bandwidth_display'),
                            link.get('status_admin'),
                            link.get('reference_partner')
                        ])
                messagebox.showinfo("Succès", f"Inventaire exporté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'écrire le fichier : {e}")

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
        self.btn_mon = ctk.CTkButton(self.tab_supervision, text="Rafraîchir Statut", fg_color=config.COLORS["primary"], command=self.fetch_monitoring_data)
        self.btn_mon.pack(pady=20)

    def go_to_monitoring(self, link):
        self.tabview.set("Supervision")
        self.label_client.configure(text=f"Client : {link.get('client_name')}")
        self.label_address.configure(text=f"Adresse : {link.get('address')}")
        self.label_status.configure(text="Chargement...", text_color=config.COLORS["text"])
        self.fetch_monitoring_data()

    def fetch_monitoring_data(self):
        """Utilise l'API_Client pour récupérer l'état du lien"""
        try:
            lien = self.api.get_monitoring_data()
            
            if lien.get('address'):
                self.label_address.configure(text=f"Adresse : {lien.get('address')}")
            
            status = str(lien.get('status_display', 'inconnu')).lower()
            color = config.COLORS["accent"] if status == 'ok' else config.COLORS["error"]
            self.label_status.configure(text=f"STATUT : {status.upper()}", text_color=color)
            
        except Exception as e:
            self.label_status.configure(text="Erreur Supervision", text_color="red")
            print(f"Erreur API Monitoring : {e}")

    def auto_refresh_monitoring(self):
        if self.label_address.cget("text") != "":
            self.fetch_monitoring_data()
        self.after(60000, self.auto_refresh_monitoring)

    def show_message(self, msg):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.scroll_frame, text=msg).pack(pady=20)