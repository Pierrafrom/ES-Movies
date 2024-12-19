from backend.models.python.User import User
from backend.config.constants import CACHE_PATH
from backend.services.movie_loader import load_movies


def get_movies_from_cache_as_lisp(cache_path: str = CACHE_PATH) -> str:
    """
    Génère une liste Lisp à partir des films du cache.

    :param cache_path: Chemin vers le fichier de cache JSON.
    :return: Une chaîne contenant la liste des films au format Lisp.
    """
    # movies_data = load_cache(cache_path)
    movies_data = load_movies(2000, True, False)
    lisp_movies = [m.to_lisp() for m in movies_data]
    return "(" + " ".join(lisp_movies) + ")"


def get_data_as_lisp(cache_path: str, user: User) -> str:
    """
    Génère une structure Lisp contenant les films en `car` et l'utilisateur en `cdr`.

    :param cache_path: Chemin vers le fichier de cache JSON.
    :param user: Instance de la classe User.
    :return: Une chaîne contenant les films et l'utilisateur au format Lisp.
    """

    movies_list = get_movies_from_cache_as_lisp(cache_path)

    # Utilisateur
    user_lisp = user.to_lisp()

    # Structure complète
    return f"({movies_list} . {user_lisp})"
