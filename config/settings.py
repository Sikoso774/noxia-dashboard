import os
import sys
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent.parent

BASE_DIR = get_base_path()
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # On utilise Field pour être explicite et permettre des valeurs par défaut si besoin
    BASE_URL: str = Field(validation_alias="BASE_URL")
    API_KEY: str = Field(validation_alias="KISSGROUP_API_KEY")

    model_config = SettingsConfigDict(
            env_file=str(ENV_PATH),
            env_file_encoding='utf-8',
            extra='ignore',
            # On dit à Pydantic de prioriser le fichier .env sur les variables système
            env_priority=1 
        )


# Instanciation globale
try:
    settings = Settings()
except Exception as e:
    print(f"ERREUR instanciation de Settings : {e}")

# --- CHARTE GRAPHIQUE NOXIA SECURITY ---
COLORS = {
    "bg": "#121212",
    "card": "#2b2b2b",
    "primary": "#1f538d",
    "accent": "#2ecc71",
    "error": "#e74c3c",
    "text": "#ffffff",
    "border": "#3d3d3d"
}

# --- RÉGLAGES ASSETS ---
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
LOGO_FILENAME = "logo-noxia.png"
LOGO_WIDTH = 400