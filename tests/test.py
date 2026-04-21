import requests
import customtkinter as ctk

# Configuration API
BASE_URL = "https://kissapi.kissgroup.io/kisslink"
API_KEY = "019dab34-0a36-74f5-98cc-efe55ee79d21"

class NoxiaDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Noxia Security - Gestion des Liens Kissgroup")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        # --- UI Layout ---
        self.header = ctk.CTkLabel(self, text="Inventaire des Liens", font=("Arial", 24, "bold"))
        self.header.pack(pady=20)

        # Zone défilante pour la liste
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Liste des accès clients")
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.btn_load = ctk.CTkButton(self, text="Charger la liste des liens", command=self.load_links)
        self.btn_load.pack(pady=20)

    def clear_frame(self):
        """Nettoie la liste avant un rafraîchissement"""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def load_links(self):
        """Récupère et affiche la liste des liens depuis l'API"""
        self.clear_frame()
        headers = {"api_key": API_KEY}
        
        try:
            # Appel à l'endpoint /links [cite: 4, 6]
            response = requests.get(f"{BASE_URL}/links", headers=headers)
            response.raise_for_status()
            links_data = response.json() # Récupère la liste 

            if not links_data:
                self.show_message("Aucun lien trouvé.")
                return

            for i, link in enumerate(links_data):
                self.create_link_card(link, i)

        except Exception as e:
            self.show_message(f"Erreur : {str(e)}")

    def create_link_card(self, link, index):
        """Crée un petit bloc visuel pour chaque lien"""
        card = ctk.CTkFrame(self.scroll_frame)
        card.pack(fill="x", padx=10, pady=5)

        # Colonne 1 : Client et Code
        name_label = ctk.CTkLabel(card, text=f"{link.get('client_name')}", font=("Arial", 14, "bold"))
        name_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        code_label = ctk.CTkLabel(card, text=f"Code: {link.get('link_code')}", text_color="gray")
        code_label.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")

        # Colonne 2 : Technologie et Débit 
        tech_info = f"{link.get('techno_name')} - {link.get('bandwidth_display')}"
        tech_label = ctk.CTkLabel(card, text=tech_info)
        tech_label.grid(row=0, column=1, padx=20, sticky="e")

        # Colonne 3 : Statut Administratif 
        status = link.get('status_admin', 'Inconnu')
        status_color = "#2ecc71" if status == "Livré" else "#f1c40f"
        status_label = ctk.CTkLabel(card, text=status, text_color=status_color, font=("Arial", 12, "bold"))
        status_label.grid(row=0, column=2, padx=20, sticky="e")
        
        # On ajuste les colonnes pour un bel alignement
        card.grid_columnconfigure(0, weight=1)

    def show_message(self, msg):
        lbl = ctk.CTkLabel(self.scroll_frame, text=msg)
        lbl.pack(pady=20)

if __name__ == "__main__":
    app = NoxiaDashboard()
    app.mainloop()