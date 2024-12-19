from dotenv import load_dotenv
import os
from backend.config.constants import ENV_PATH

# Charger les variables d'environnement à partir du fichier .env
# load_dotenv(dotenv_path=ENV_PATH)

# ----------------------------------------------------------------------------------------------------------------------
# Prod
# ----------------------------------------------------------------------------------------------------------------------

def get_api_key():
    api_key = os.getenv("API_KEY")
    print(f"Retrieved API_KEY: {api_key}")  # Debug log
    if not api_key:
        raise Exception("API Key not found. Please set it in the .env file.")
    return api_key

# ----------------------------------------------------------------------------------------------------------------------
# Dev
# ----------------------------------------------------------------------------------------------------------------------

'''
def get_api_key() -> str:
    """
    Reads the TMDb API key from the .env file.

    :return: The TMDb API key as a string.
    :raises Exception: If the API key is not found in the environment.
    """
    api_key = os.getenv("TMDB_API_KEY")  # Récupère la clé API
    if not api_key:
        raise Exception("API Key not found. Please set it in the .env file.")
    return api_key
'''