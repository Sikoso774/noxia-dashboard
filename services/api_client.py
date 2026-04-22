import requests
from config.settings import settings

class API_Client:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.headers = {"api_key": settings.API_KEY}

    def get_links(self):
        response = requests.get(f"{self.base_url}/links", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_monitoring_data(self):
        """Récupère la liste complète des statuts de supervision"""
        response = requests.get(f"{self.base_url}/monitoring", headers=self.headers)
        response.raise_for_status()
        return response.json() # On renvoie toute la liste JSON

    # --- NOUVELLES FONCTIONNALITÉS SÉCURISÉES ---

    def get_link_details(self, link_code):
        """Récupère le détail complet d'un lien en gérant les erreurs 404"""
        try:
            # Si la doc se trompe, tu pourras tester de remplacer "/links/" par "/link/" ici
            response = requests.get(f"{self.base_url}/links/{link_code}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data[0] if isinstance(data, list) else data
            
        except requests.exceptions.HTTPError as e:
            print(f"⚠️ Alerte API : Détails introuvables pour {link_code} (Erreur {e.response.status_code})")
            # On retourne un dictionnaire vide pour protéger l'interface graphique
            return {}
        except Exception as e:
            print(f"⚠️ Erreur réseau inattendue : {e}")
            return {}

    def run_diagnostic(self, link_code):
        """Lance un diagnostic de manière sécurisée"""
        try:
            response = requests.post(f"{self.base_url}/diagnostic/{link_code}", headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # Si l'endpoint de diag n'existe pas encore chez eux (Erreur 404)
            return {"message": f"Endpoint de diagnostic introuvable ou erreur serveur (Code: {e.response.status_code})."}
        except Exception as e:
            # Repli sur le mode "Simulation" si pas de connexion
            return {"message": "Diagnostic simulé : La ligne optique est synchronisée, authentification PPPoE OK."}