import customtkinter as ctk
import keyring
from config.settings import COLORS, FONTS

class SetupFrame(ctk.CTkFrame):
    def __init__(self, master, on_success, **kwargs):
        # On hérite de CTkFrame et on prend tout l'espace
        super().__init__(master, fg_color=COLORS["bg"], **kwargs)
        self.on_success = on_success # Fonction à appeler une fois fini
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Contenu identique à ton ancienne fenêtre mais dans un Frame"""
        ctk.CTkLabel(self, text="🔐 CONFIGURATION SÉCURISÉE", font=FONTS["title"]).pack(pady=40)
        
        ctk.CTkLabel(self, text="Veuillez saisir votre clé API Kissgroup :", font=FONTS["body"]).pack(pady=10)
        
        self.api_key_entry = ctk.CTkEntry(self, width=300, placeholder_text="Clé API...", show="*")
        self.api_key_entry.pack(pady=10, padx=20)

        self.save_btn = ctk.CTkButton(
            self, text="ENREGISTRER", 
            command=self._save_key,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"]
        )
        self.save_btn.pack(pady=20)

        self.info_label = ctk.CTkLabel(self, text="", font=FONTS["small"])
        self.info_label.pack()

    def _save_key(self) -> None:
        key = self.api_key_entry.get().strip()
        if not key:
            self.info_label.configure(text="❌ Saisie vide", text_color=COLORS["error"])
            return

        try:
            # Sauvegarde sécurisée
            keyring.set_password("NoxiaDashboard", "API_KEY", key)
            self.info_label.configure(text="✅ Succès !", text_color=COLORS["accent"])
            
            # On avertit l'application principale qu'on a fini
            self.after(500, lambda: self.on_success(key))
        except Exception as e:
            self.info_label.configure(text=f"❌ Erreur : {e}", text_color=COLORS["error"])