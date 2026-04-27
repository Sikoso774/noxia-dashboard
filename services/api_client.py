"""Module responsable des communications HTTP avec l'API métier Noxia.

Ce module encapsule la bibliothèque 'requests' pour fournir des méthodes
de haut niveau permettant de récupérer les liens, le monitoring et les détails.
"""

import time
from typing import Any, Dict, List, Union
import requests

from config.settings import settings
from config.logger import setup_logger

# Initialisation du logger pour ce module spécifique
logger = setup_logger("API_Client")


class API_Client:
    """Client HTTP dédié aux échanges avec l'API Noxia.

    Gère l'authentification via clé d'API, le maintien de la session (Keep-Alive)
    et la construction des requêtes GET sécurisées.

    Attributes:
        base_url (str): URL racine de l'API (issue des configurations).
        session (requests.Session): Objet session pour mutualiser les connexions.
        timeout (int): Temps d'attente maximum pour une réponse (en secondes).
    """

    def __init__(self) -> None:
        """Initialise le client API avec les en-têtes de sécurité."""
        self.base_url: str = settings.BASE_URL
        self.session: requests.Session = requests.Session()
        
        # Configuration des en-têtes par défaut pour la session
        self.session.headers.update({
            "User-Agent": "NoxiaSecurityDashboard/1.0",
            "Accept": "application/json",
            "api_key": settings.API_KEY
        })
        
        self.timeout: int = 10
        logger.info("API_Client sécurisé initialisé avec succès")

    def get_links(self) -> List[Dict[str, Any]]:
        """Récupère la liste complète des liens réseau.

        Returns:
            List[Dict[str, Any]]: Liste de dictionnaires représentant chaque lien.

        Raises:
            requests.exceptions.RequestException: En cas d'erreur de communication.
        """
        try:
            logger.debug("Tentative de récupération de la liste des liens...")
            response = self.session.get(f"{self.base_url}/links", timeout=self.timeout)
            response.raise_for_status()
            links: List[Dict[str, Any]] = response.json()
            logger.info(f"{len(links)} liens récupérés avec succès")
            return links
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des liens : {e}")
            raise

    def get_monitoring_data(self) -> List[Dict[str, Any]]:
        """Récupère les données de supervision (monitoring) pour l'ensemble des liens.

        Returns:
            List[Dict[str, Any]]: Liste des métriques de monitoring reçues.
        """
        try:
            logger.debug("Appel API : /monitoring")
            response = self.session.get(
                f"{self.base_url}/monitoring", 
                timeout=self.timeout, 
                verify=True
            )
            response.raise_for_status()
            data: List[Dict[str, Any]] = response.json()
            logger.info("Données de monitoring reçues")
            return data
        except Exception as e:
            logger.error(f"Erreur monitoring : {e}")
            return []

    def get_link_details(self, link_code: str) -> Dict[str, Any]:
        """Récupère les informations techniques détaillées pour un lien spécifique.

        Args:
            link_code (str): Identifiant unique (code) du lien réseau.

        Returns:
            Dict[str, Any]: Dictionnaire contenant les détails techniques.
            Retourne un dictionnaire vide si le lien est introuvable.
        """
        try:
            logger.debug(f"Récupération des détails pour le lien : {link_code}")
            response = self.session.get(f"{self.base_url}/links/{link_code}", timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Détails récupérés pour {link_code}")
            details: Dict[str, Any] = response.json()
            return details
        except requests.exceptions.HTTPError:
            logger.warning(f"Lien {link_code} introuvable (404) ou erreur API")
            return {}
        except Exception as e:
            logger.error(f"Erreur réseau sur {link_code} : {e}")
            return {}