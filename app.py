import os
import requests
import csv
import customtkinter as ctk
from PIL import Image
from dotenv import load_dotenv
from tkinter import filedialog, messagebox

load_dotenv()

# --- CONFIGURATION IDENTITÉ VISUELLE NOXIA ---
COLORS = {
    "bg": "#121212",
    "card": "#2b2b2b",
    "primary": "#1f538d",
    "accent": "#2ecc71",
    "error": "#e74c3c",
    "text": "#ffffff",
    "border": "#3d3d3d"
}

BASE_URL = "https://kissapi.kissgroup.io/kisslink"
API_KEY = os.getenv("KISSGROUP_API_KEY")

class NoxiaDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Noxia Security - Dashboard")
        self.geometry("1000x800")
        self.configure(fg_color=COLORS["bg"])

        self.all_links = [] # Cache pour l'export et la recherche

        # --- HEADER AVEC LOGO ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20, padx=20, fill="x")

        try:
            basedir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(basedir, "logo-noxia.png") 
            pil_img = Image.open(logo_path)
            
            width_wanted = 400
            ratio = pil_img.height / pil_img.width
            height_calculated = int(width_wanted * ratio)
            
            logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(width_wanted, height_calculated))
            self.logo_label = ctk.CTkLabel(self.header_frame, image=logo_img, text="")
            self.logo_label.pack(side="left", padx=(0, 20))
        except Exception as e:
            print(f"Erreur logo : {e}")

        # --- ONGLETS ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color=COLORS["primary"])
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.tab_liste = self.tabview.add("Liste des Liens")
        self.tab_supervision = self.tabview.add("Supervision")

        self.setup_tab_liste()
        self.setup_tab_supervision()
        self.auto_refresh_monitoring()

    def setup_tab_liste(self):
        # Frame de contrôle (Recherche + Boutons)
        self.ctrl_frame = ctk.CTkFrame(self.tab_liste, fg_color="transparent")
        self.ctrl_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(self.ctrl_frame, placeholder_text="Rechercher...", width=350, height=35)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_links)

        # Bouton Charger
        self.btn_load = ctk.CTkButton(self.ctrl_frame, text="CHARGER API", fg_color=COLORS["primary"], command=self.load_links)
        self.btn_load.pack(side="left", padx=5)

        # Bouton Exporter CSV
        self.btn_export = ctk.CTkButton(self.ctrl_frame, text="EXPORTER CSV", fg_color="#27ae60", hover_color="#1e8449", command=self.export_to_csv)
        self.btn_export.pack(side="left", padx=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_liste, fg_color="transparent")
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def load_links(self):
        """Récupère les liens depuis l'API /links"""
        headers = {"api_key": API_KEY}
        try:
            response = requests.get(f"{BASE_URL}/links", headers=headers)
            response.raise_for_status()
            self.all_links = response.json()
            self.display_links(self.all_links)
        except Exception as e:
            self.show_message(f"Erreur : {e}")

    def display_links(self, links_to_show):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        for link in links_to_show:
            card = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["card"], border_width=1, border_color=COLORS["border"])
            card.pack(fill="x", padx=10, pady=5)

            info = f"{link.get('client_name')}\n{link.get('link_code')} | {link.get('techno_name')}"
            ctk.CTkLabel(card, text=info, font=("Arial", 13, "bold"), justify="left").pack(side="left", padx=15, pady=10)

            status = link.get('status_admin')
            color = COLORS["accent"] if status == "Livré" else "#f1c40f"
            ctk.CTkLabel(card, text=f"● {status}", text_color=color).pack(side="left", padx=20)

            ctk.CTkButton(card, text="SUPERVISER", width=100, fg_color=COLORS["primary"],
                          command=lambda l=link: self.go_to_monitoring(l)).pack(side="right", padx=15)

    def filter_links(self, event=None):
        query = self.search_entry.get().lower()
        filtered = [l for l in self.all_links if query in str(l).lower()]
        self.display_links(filtered)

    def export_to_csv(self):
        """Exporte l'inventaire actuel en fichier CSV"""
        if not self.all_links:
            messagebox.showwarning("Export Impossible", "Veuillez d'abord charger la liste des liens via l'API.")
            return

        # Demande à l'utilisateur où enregistrer le fichier
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
                    # En-têtes basés sur la doc 
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
                messagebox.showinfo("Succès", f"Inventaire exporté avec succès vers :\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'écrire le fichier : {e}")

        

    def setup_tab_supervision(self):
        self.label_client = ctk.CTkLabel(self.tab_supervision, text="Sélectionnez un lien dans la liste.", font=("Arial", 14))
        self.label_client.pack(pady=(40, 10))
        self.label_address = ctk.CTkLabel(self.tab_supervision, text="", font=("Arial", 12))
        self.label_address.pack(pady=10)
        self.label_status = ctk.CTkLabel(self.tab_supervision, text="-", font=("Arial", 25, "bold"))
        self.label_status.pack(pady=30)
        self.btn_mon = ctk.CTkButton(self.tab_supervision, text="Rafraîchir Statut", fg_color=COLORS["primary"], command=self.fetch_monitoring_data)
        self.btn_mon.pack(pady=20)

    def fetch_monitoring_data(self):
        """Récupère les données temps réel et met à jour TOUS les labels"""
        headers = {"api_key": API_KEY}
        try:
            response = requests.get(f"{BASE_URL}/monitoring", headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # L'API renvoie un objet ou une liste 
            lien = data[0] if isinstance(data, list) else data
            
            # Mise à jour de l'adresse et du client depuis les données de monitoring 
            if lien.get('address'):
                self.label_address.configure(text=f"Adresse : {lien.get('address')}")
            
            # Mise à jour du statut visuel
            status = str(lien.get('status_display', 'inconnu')).lower()
            color = COLORS["accent"] if status == 'ok' else COLORS["error"]
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

if __name__ == "__main__":
    app = NoxiaDashboard()
    app.mainloop()