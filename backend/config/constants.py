import os

# Project base directory (one level up from the current directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# .env file path
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))

# Path to the cache directory and cache file
CACHE_DIR = os.path.join(BASE_DIR, "data")
CACHE_FILE = "movies_cache.json"
CACHE_PATH = os.path.join(CACHE_DIR, CACHE_FILE)

# API base URL and endpoint for popular movies
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POPULAR_MOVIES_URL = f"{TMDB_BASE_URL}/movie/popular"
SEARCH_MOVIE_URL = f"{TMDB_BASE_URL}/search/movie"
DISCOVER_MOVIES_URL = f"{TMDB_BASE_URL}/discover/movie"

# Default settings for the API (language and region)
DEFAULT_LANGUAGE = "fr-FR"  # French
DEFAULT_REGION = "FR"       # France


EXPERT_SYSTEM_LISP_PATH = os.path.join(BASE_DIR, "expert_system", "expert_system.lisp")
SBCL_EXECUTABLE = "/usr/bin/sbcl"