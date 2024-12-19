import os
import requests
from typing import List, Dict
from backend.utils.cache_manager import load_cache, save_cache
from backend.utils.api_key_manager import get_api_key
from backend.models.python.Movie import Movie
from backend.config.constants import DEFAULT_LANGUAGE, DEFAULT_REGION, POPULAR_MOVIES_URL, CACHE_PATH, BASE_DIR, CACHE_DIR


# ---------------------------------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------------------------------

def fetch_movies_from_api(number_of_movies: int) -> List[Dict]:
    """
    Fetch popular movies from the TMDB API.

    :param number_of_movies: The number of movies to fetch.
    :return: A list of dictionaries containing movie details.
    """
    api_key = get_api_key()  # Retrieve the API key from environment variables
    fetched_movies = []  # List to hold fetched movies
    page = 1  # API pagination starts at page 1

    # Keep fetching until the required number of movies is obtained
    while len(fetched_movies) < number_of_movies:
        # API request parameters
        params = {
            "api_key": api_key,
            "language": DEFAULT_LANGUAGE,
            "region": DEFAULT_REGION,
            "page": page
        }

        # Perform the GET request to the API
        response = requests.get(POPULAR_MOVIES_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        # Extract movie results from the API response
        data = response.json()
        fetched_movies += data.get("results", [])
        page += 1  # Move to the next page

    return fetched_movies[:number_of_movies]


def update_cache_incrementally(new_movies: List[Dict], cache_path: str):
    """
    Update the movie cache incrementally by adding only new movies.

    :param new_movies: List of movies retrieved from the API.
    :param cache_path: Path to the cache file.
    """
    # Load the existing cache (if it exists)
    existing_movies = load_cache(cache_path)
    existing_ids = {m.get("id") for m in existing_movies}  # Set of existing movie IDs

    # Add only new movies that are not already in the cache
    updated_movies = existing_movies.copy()
    for m in new_movies:
        if m.get("id") not in existing_ids:
            updated_movies.append(m)

    # Save the updated cache back to the file
    print(f"Adding {len(updated_movies) - len(existing_movies)} new movies to the cache.")
    save_cache(updated_movies, cache_path)


def load_movies(number_of_movies: int, use_cache: bool, update_cache: bool) -> List[Movie]:
    """
    Load movies either from the cache or the TMDB API.

    :param number_of_movies: Number of movies to load.
    :param use_cache: If True, load movies from the cache; otherwise, fetch from the API.
    :param update_cache: If True, update the cache incrementally with new movies.
    :return: A list of Movie objects.
    """
    if use_cache and os.path.exists(CACHE_PATH):
        print("Loading movies from cache...")
        movies_data = load_cache(CACHE_PATH)
    else:
        print("Fetching movies from the TMDB API...")
        movies_data = fetch_movies_from_api(number_of_movies)

        # Update the cache incrementally if requested
        if update_cache:
            print("Updating cache incrementally...")
            update_cache_incrementally(movies_data, CACHE_PATH)

    # Convert the loaded movie data into a list of Movie objects
    loaded_movies = [Movie.from_dict(m) for m in movies_data[:number_of_movies]]
    return loaded_movies


# ---------------------------------------------------------------------------------------------------
# Main Execution Block
# ---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Example usage of the movie loader script.
    """
    # Display base and cache directory paths
    print(f"Base Directory: {BASE_DIR}")
    print(f"Cache Directory: {CACHE_DIR}")

    # User-defined parameters
    NUMBER_OF_MOVIES = 10000  # Number of movies to load
    USE_CACHE = False  # Use cached data if available
    UPDATE_CACHE = True  # Update the cache incrementally after fetching from the API

    # Load the movies based on the defined parameters
    try:
        movies = load_movies(NUMBER_OF_MOVIES, USE_CACHE, UPDATE_CACHE)
        for movie in movies:
            print(movie)
    except Exception as e:
        print(f"Error: {e}")
