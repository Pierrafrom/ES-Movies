import os
import json
from typing import List, Dict


def load_cache(file_path: str) -> List[Dict]:
    """
    Load cached movie data from a specified JSON file.

    :param file_path: The path to the cache file.
    :return: A list of cached movies as dictionaries.
    """

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_cache(movies: List[Dict], file_path: str):
    """
    Save movie data to a specified JSON cache file.

    :param movies: A list of movie data as dictionaries.
    :param file_path: The full path to the cache file.
    """

    # Crée le répertoire parent s'il n'existe pas
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("trying to save cache in " + file_path)

    # Écrit les données dans le fichier
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
