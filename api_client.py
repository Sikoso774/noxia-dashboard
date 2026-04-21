import requests

class API_Client:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        # L'API filtrera automatiquement les liens grâce à ce header [cite: 3]
        self.headers = {"api_key": api_key}

    def get_links(self):
        """Retourne l'ensemble des liens rattachés à votre partenaire [cite: 6]"""
        response = requests.get(f"{self.base_url}/links", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_monitoring_data(self):
        """Récupère les données de supervision en temps réel"""
        response = requests.get(f"{self.base_url}/monitoring", headers=self.headers)
        response.raise_for_status()
        data = response.json()
        
        # Gestion du format : retourne le premier élément si c'est une liste
        return data[0] if isinstance(data, list) else data