import json
import os
import subprocess
from typing import Optional, Dict, Any

import requests

from backend.config.constants import CACHE_PATH, SEARCH_MOVIE_URL, DEFAULT_LANGUAGE, EXPERT_SYSTEM_LISP_PATH, \
    SBCL_EXECUTABLE
from backend.models.python.Movie import Movie
from backend.utils.api_key_manager import get_api_key
from backend.utils.cache_manager import load_cache, save_cache


def fetch_movie_by_title(title: str) -> Optional[Movie]:
    """
    Fetch a movie by its title. Search first in the cache, then in the API.

    :param title: The title of the movie to search for.
    :return: An instance of Movie if found, else None.
    """
    # Load cache data
    cache_data = load_cache(CACHE_PATH)

    # Search in cache
    for movie_data in cache_data:
        if movie_data.get("title", "").lower() == title.lower():
            print("Movie found in cache.")
            return Movie.from_dict(movie_data)

    # If not found in cache, search in API
    print("Movie not found in cache. Searching in API...")
    api_key = get_api_key()
    params = {
        "api_key": api_key,
        "query": title,
        "language": DEFAULT_LANGUAGE
    }
    response = requests.get(SEARCH_MOVIE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    results = response.json().get("results", [])
    if not results:
        print("No results found in API.")
        return None

    # If multiple results, return the first
    selected_movie = results[0]
    print(f"Movie '{selected_movie['title']}' found in API.")

    # Add to cache
    cache_data.append(selected_movie)
    save_cache(cache_data, CACHE_PATH)

    return Movie.from_dict(selected_movie)


def call_expert_system(lisp_data: str, lisp_script_path: str = EXPERT_SYSTEM_LISP_PATH) -> Dict[str, Any]:
    """
    Calls the expert system by executing the provided Lisp script with the given S-expression data.

    Args:
        lisp_data (str): The S-expression Lisp data to send to the expert system.
        lisp_script_path (str, optional): The absolute path to the Lisp script. Defaults to EXPERT_SYSTEM_LISP_PATH.

    Returns:
        Dict[str, Any]: The JSON response from the expert system.

    Raises:
        FileNotFoundError: If SBCL is not installed or the Lisp script is not found.
        subprocess.SubprocessError: If an error occurs during the subprocess execution.
        json.JSONDecodeError: If the expert system's output is not valid JSON.
        ValueError: If input data is not a string.
        AttributeError: If the input data does not have a to_lisp() method.
        Exception: For any other unexpected errors.
    """
    # Validate input
    if not isinstance(lisp_data, str):
        raise ValueError("Lisp data must be a string.")

    if not os.path.isfile(lisp_script_path):
        raise FileNotFoundError(f"Lisp script '{lisp_script_path}' not found.")

    try:
        # Execute the Lisp script as a subprocess
        process = subprocess.Popen(
            [SBCL_EXECUTABLE, "--script", lisp_script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send Lisp data via stdin
        stdout, stderr = process.communicate(input=lisp_data)

        # Check for subprocess errors
        if process.returncode != 0:
            raise subprocess.SubprocessError(f"Error in Lisp script: {stderr.strip()}")

        # Parse the JSON response
        try:
            json_response = json.loads(stdout)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Failed to parse JSON: {e.msg}", e.doc, e.pos)

        return json_response

    except FileNotFoundError:
        raise FileNotFoundError("SBCL not found. Please install SBCL and ensure it is in your PATH.")
    except subprocess.SubprocessError as e:
        raise e
    except json.JSONDecodeError as e:
        raise e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")


