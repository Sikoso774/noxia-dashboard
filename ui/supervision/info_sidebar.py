"""Module contenant la barre latérale d'information pour la supervision.

Ce panneau affiche les détails du lien (adresse, état, statistiques matérielles)
ainsi que les contrôles pour lancer des actions comme le diagnostic.
"""

from typing import Any, Callable, Dict, Optional, Tuple
import tkinter.filedialog as fd
import customtkinter as ctk
from config.settings import COLORS, FONTS


class InfoSidebar(ctk.CTkScrollableFrame):
    """Panneau latéral défilant affichant les détails d'un lien réseau.

    Cette classe hérite de CTkScrollableFrame pour permettre de faire défiler
    les nombreuses informations techniques.

    Attributes:
        label_client (ctk.CTkLabel): Affiche le nom du client.
        label_address (ctk.CTkLabel): Affiche l'adresse d'installation.
        tech_frame (ctk.CTkFrame): Conteneur pour les informations techniques.
        btn_refresh (ctk.CTkButton): Bouton pour actualiser les données.
        btn_diag (ctk.CTkButton): Bouton pour lancer un diagnostic métier.
        progress_bar (ctk.CTkProgressBar): Barre d'attente pour le diagnostic.
        diag_result (ctk.CTkTextbox): Zone de texte pour afficher les résultats réseau.
    """

    def __init__(
        self,
        master: Any,
        on_refresh: Callable[[], None],
        on_diagnostic: Callable[[], None],
        **kwargs: Any
    ) -> None:
        """Initialise la barre d'information avec ses sous-composants.

        Args:
            master (Any): Widget parent (typiquement un CTkFrame ou la fenêtre principale).
            on_refresh (Callable[[], None]): Callback exécuté au clic sur "Rafraîchir Statut".
            on_diagnostic (Callable[[], None]): Callback exécuté au clic sur "LANCER DIAGNOSTIC".
            **kwargs (Any): Arguments supplémentaires passés au constructeur CTkScrollableFrame.
        """
        super().__init__(
            master,
            width=320,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scroll_button"],
            scrollbar_button_hover_color=COLORS["scroll_hover"],
            **kwargs
        )

        # En-tête Client
        self.label_client = ctk.CTkLabel(
            self, text="Sélectionnez un lien", font=FONTS["title"], wraplength=280
        )
        self.label_client.pack(pady=(10, 5))

        self.label_address = ctk.CTkLabel(
            self, text="", font=FONTS["body"], wraplength=280
        )
        self.label_address.pack(pady=5)

        # Carte d'informations techniques
        self.tech_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=8)
        self.tech_frame.pack(fill="x", pady=15, padx=5)

        self.label_last_conn = self._create_label(
            "Dernière connexion : -", bold=True, color=COLORS["accent"]
        )
        self.label_provider = self._create_label("Fournisseur : -")
        self.label_ip = self._create_label("IP Publique : -")
        self.label_pppoe = self._create_label("Session PPP : -")
        self.label_brand = self._create_label("Marque : -")
        self.label_attenuation = self._create_label("Atténuation : -", bold=True)
        self.label_pass = self._create_label("Pass Admin : -", padding=(2, 10))

        # Statut Temps Réel
        self.label_status = ctk.CTkLabel(self, text="-", font=FONTS["status"])
        self.label_status.pack(pady=15)

        # Bouton Rafraîchir
        self.btn_refresh = ctk.CTkButton(
            self,
            text="Rafraîchir Statut",
            font=FONTS["button"],
            width=0,  # S'adapte à la longueur du texte
            fg_color=COLORS["card"],
            hover_color=COLORS["card_alt"],
            border_width=1,
            border_color=COLORS["primary"],
            command=on_refresh
        )
        self.btn_refresh.pack(pady=10)

        # Bouton Diagnostic
        self.btn_diag = ctk.CTkButton(
            self,
            text="LANCER DIAGNOSTIC",
            font=FONTS["button"],
            width=0,  # S'adapte à la longueur du texte
            fg_color=COLORS["card"],
            hover_color=COLORS["card_alt"],
            border_width=1,
            border_color=COLORS["primary"],
            command=on_diagnostic
        )
        self.btn_diag.pack(pady=(15, 25))

        # Création de la barre de progression (cachée par défaut)
        self.progress_bar = ctk.CTkProgressBar(
            self,
            orientation="horizontal",
            mode="indeterminate",
            progress_color=COLORS["accent"],
            fg_color=COLORS["card"]
        )
        self.progress_bar.set(0)

        # Zone de résultat Diagnostic
        self.diag_result = ctk.CTkTextbox(
            self, height=100, fg_color=COLORS["card"], state="disabled", wrap="word"
        )
        self.diag_result.pack(fill="x", pady=5, padx=5)

        # Actions d'export (Copier / Sauvegarder)
        self.export_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.export_frame.pack(fill="x", pady=(0, 15), padx=5)

        self.btn_save = ctk.CTkButton(
            self.export_frame,
            text="💾",
            font=FONTS["button"],
            width=40,
            fg_color=COLORS["card"],
            hover_color=COLORS["card_alt"],
            border_width=1,
            border_color=COLORS["primary"],
            command=self._save_to_file
        )
        self.btn_save.pack(side="right", padx=(5, 0))

        self.btn_copy = ctk.CTkButton(
            self.export_frame,
            text="📄",
            font=FONTS["button"],
            width=40,
            fg_color=COLORS["card"],
            hover_color=COLORS["card_alt"],
            border_width=1,
            border_color=COLORS["primary"],
            command=self._copy_to_clipboard
        )
        self.btn_copy.pack(side="right", padx=(5, 5))

    def _create_label(
        self,
        text: str,
        bold: bool = False,
        color: Optional[str] = None,
        padding: Tuple[int, int] = (2, 2)
    ) -> ctk.CTkLabel:
        """Méthode utilitaire interne pour générer des labels harmonisés.

        Args:
            text (str): Texte à afficher.
            bold (bool, optional): Utilise la police 'subtitle' si True, 'body' sinon. Par défaut False.
            color (Optional[str], optional): Couleur hexadécimale du texte. Par défaut None.
            padding (Tuple[int, int], optional): Marges externes Y (haut, bas). Par défaut (2, 2).

        Returns:
            ctk.CTkLabel: Le label instancié et packé dans tech_frame.
        """
        if color is None:
            color = COLORS["text_sub"]
            
        font = FONTS["subtitle"] if bold else FONTS["body"]
        lbl = ctk.CTkLabel(
            self.tech_frame, text=text, font=font, text_color=color, anchor="w"
        )
        lbl.pack(fill="x", padx=10, pady=padding)
        return lbl

    def update_display(self, data: Dict[str, Any]) -> None:
        """Met à jour l'ensemble des labels avec les données récupérées depuis l'API.

        Args:
            data (Dict[str, Any]): Dictionnaire contenant les métriques d'un lien.
        """
        status_text: str = data.get("status", "INCONNU").strip().upper()
        is_ok: bool = (status_text == "OK")

        self.label_status.configure(
            text=f"STATUT : {status_text}",
            text_color=COLORS["accent"] if is_ok else COLORS["error"]
        )

        self.label_address.configure(text=f"Adresse : {data.get('address', '')}")
        self.label_ip.configure(text=f"IP Publique : {data.get('ip_publique', 'N/A')}")
        self.label_pppoe.configure(text=f"Session PPP : {data.get('session_ppp', 'N/A')}")
        self.label_provider.configure(text=f"Fournisseur : {data.get('provider', 'N/A')}")
        self.label_brand.configure(text=f"Marque : {data.get('brand', 'N/A')}")
        self.label_pass.configure(text=f"Pass Admin : {data.get('password_device', 'N/A')}")

        # Gestion de la date de dernière connexion
        last_conn: str = data.get("last_change_connection_date", "Inconnue")
        if "T" in last_conn:
            # Conversion basique du format ISO
            parts = last_conn.split("T")
            formatted_date = f"{parts[0]} à {parts[1][:5]}"
        else:
            formatted_date = last_conn
            
        self.label_last_conn.configure(text=f"Dernière co : {formatted_date}")

        # Alerte atténuation (rouge si en dessous de -20 dB)
        att = data.get("attenuation", 0)
        try:
            att_val = float(att)
        except (ValueError, TypeError):
            att_val = 0
            
        self.label_attenuation.configure(
            text=f"Atténuation : {att} dB",
            text_color=COLORS["accent"] if att_val >= -20 else COLORS["error"]
        )

    def set_diag_text(self, text: str) -> None:
        """Insère du texte dans la zone de résultat de diagnostic de façon sécurisée.

        Args:
            text (str): Le contenu (logs ou rapport) à afficher.
        """
        self.diag_result.configure(state="normal")
        self.diag_result.delete("1.0", "end")
        self.diag_result.insert("1.0", text)
        self.diag_result.configure(state="disabled")

    def start_loading(self) -> None:
        """Affiche et anime la barre de progression lors d'une tâche lourde.
        
        Bloque également le bouton de diagnostic pour éviter les clics multiples.
        """
        self.btn_diag.configure(state="disabled")
        # Insertion juste au-dessus de la textbox de résultats
        self.progress_bar.pack(pady=5, before=self.diag_result)
        self.progress_bar.start()

    def stop_loading(self) -> None:
        """Arrête et cache la barre de progression, et réactive les boutons."""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_diag.configure(state="normal")

    def _get_export_text(self) -> str:
        """Génère un rapport textuel complet (infos générales et diagnostic).

        Returns:
            str: Le texte formaté prêt à être exporté ou copié.
        """
        client = self.label_client.cget("text")
        address = self.label_address.cget("text")
        status = self.label_status.cget("text")
        
        tech_info = []
        for widget in self.tech_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                tech_info.append(widget.cget("text"))
        tech_text = "\n".join(tech_info)
        
        diag_text = self.diag_result.get("1.0", "end-1c")
        
        return (
            f"=== INFORMATIONS GENERALES ===\n"
            f"{client}\n"
            f"{address}\n\n"
            f"=== STATUT ===\n"
            f"{status}\n\n"
            f"=== DETAILS TECHNIQUES ===\n"
            f"{tech_text}\n\n"
            f"=== RESULTAT DIAGNOSTIC ===\n"
            f"{diag_text if diag_text.strip() else 'Aucun diagnostic exécuté.'}\n"
        )

    def _copy_to_clipboard(self) -> None:
        """Copie le rapport généré dans le presse-papiers du système."""
        text = self._get_export_text()
        self.clipboard_clear()
        self.clipboard_append(text)

    def _save_to_file(self) -> None:
        """Ouvre une boîte de dialogue pour enregistrer le rapport dans un fichier .txt."""
        text = self._get_export_text()
        filepath = fd.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            title="Enregistrer le rapport de diagnostic",
            initialfile="rapport_diagnostic.txt"
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde : {e}")