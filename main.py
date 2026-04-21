import requests
import customtkinter as ctk

# --- 1. Configuration de l'API ---
# Il est préférable de mettre ces infos dans un fichier .env plus tard, 
# mais on les garde ici pour le test.
API_URL = "https://kissapi.kissgroup.io/kisslink/monitoring"
API_KEY = "019dab34-0a36-74f5-98cc-efe55ee79d21" 

def fetch_data():
    """Fonction qui appelle l'API et met à jour l'interface"""
    headers = {"api_key": API_KEY}
    
    try:
        # On lance la requête GET
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status() # Lève une erreur si le statut n'est pas 200 OK
        
        # On transforme le texte brut en dictionnaire Python exploitable
        data = response.json() 
        
        # Ton log montre une structure de liste (terminée par '}]')
        if isinstance(data, list) and len(data) > 0:
            lien = data[0] # On récupère le premier lien pour l'exemple
            
            # --- 2. Mise à jour de l'interface avec les données brutes ---
            
            # Récupération de l'ID et de la référence partenaire
            label_client.configure(text=f"Lien : {lien.get('id_lien')} | Réf : {lien.get('reference_partenaire')}")
            
            # Récupération de l'adresse
            label_address.configure(text=f"Adresse : {lien.get('address')}")
            
            # Gestion visuelle du statut
            status = lien.get('status_display', 'inconnu').lower()
            if status == 'ok':
                label_status.configure(text="STATUT : OK", text_color="#2ecc71") # Vert
            else:
                label_status.configure(text=f"STATUT : {status.upper()}", text_color="#e74c3c") # Rouge
                
        else:
            label_status.configure(text="Aucune donnée trouvée.", text_color="orange")
            
    except requests.exceptions.RequestException as e:
        # Si on n'a pas internet ou que l'API est tombée
        label_status.configure(text=f"Erreur de connexion", text_color="red")
        print(f"Détail de l'erreur : {e}")

# --- 3. Création de l'interface graphique (CustomTkinter) ---

# Thème global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Création de la fenêtre principale
app = ctk.CTk()
app.geometry("550x350")
app.title("Noxia Security - Dashboard Kissgroup")

# Titre de l'application
title = ctk.CTkLabel(app, text="Supervision des liens", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(30, 20))

# Éléments de texte (vides au démarrage)
label_client = ctk.CTkLabel(app, text="Appuyez sur 'Actualiser' pour charger les données.", font=ctk.CTkFont(size=14))
label_client.pack(pady=5)

label_address = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12))
label_address.pack(pady=5)

label_status = ctk.CTkLabel(app, text="-", font=ctk.CTkFont(size=18, weight="bold"))
label_status.pack(pady=20)

# Bouton pour déclencher la fonction fetch_data()
btn_refresh = ctk.CTkButton(app, text="Actualiser les données", command=fetch_data, height=40)
btn_refresh.pack(pady=10)

# Lancement de la boucle de l'application
if __name__ == "__main__":
    app.mainloop()