from typing import List
from backend.models.python.Movie import Movie


class User:
    """
    A class to represent a user with their preferences and age.
    """

    def __init__(self, name: str, age: int):
        """
        Initializes a User instance.

        :param name: Name of the user.
        :param age: Age of the user.
        """
        self.name = name
        self.age = age
        self.favorite_movies: List[Movie] = []
        self.mood_movies: List[Movie] = []

    def set_favorite_movies(self, titles: List[str]):
        """
        Sets the user's favorite movies by querying the API or cache.
        :param titles: List of movie titles to search for.
        """
        from services.movie_selector import fetch_movie_by_title
        self.favorite_movies.clear()
        for title in titles:
            print(f"Fetching movie for title: {title}")
            movie = fetch_movie_by_title(title)
            if movie:
                print(f"Added '{movie.title}' to favorites.")
                self.favorite_movies.append(movie)
            else:
                raise Exception(f"Movie not found for title: {title}")

    def set_mood_movies(self, titles: List[str]):
        from services.movie_selector import fetch_movie_by_title
        self.mood_movies.clear()
        for title in titles:
            print(f"Fetching movie for title: {title}")
            movie = fetch_movie_by_title(title)
            if movie:
                print(f"Added '{movie.title}' to mood.")
                self.mood_movies.append(movie)
            else:
                raise Exception(f"Movie not found for title: {title}")

    def to_lisp(self) -> str:
        """
        Convert the user and their favorite movies to a Lisp s-expression.
        Example:
          (user . ((name . "Alice") (age . 25) (movies . (...)) (mood_movies . (...))))
        """
        user_part = f'(:name . "{self.name}") (:age . {self.age})'
        movies_parts = [movie.to_lisp() for movie in self.favorite_movies]
        mood_movies_parts = [movie.to_lisp() for movie in self.mood_movies]

        movies_list = "(" + " ".join(movies_parts) + ")"
        mood_movies_list = "(" + " ".join(mood_movies_parts) + ")"

        movies_part = f'(:movies . {movies_list})'
        mood_movies_part = f'(:mood_movies . {mood_movies_list})'

        return f"({user_part} {movies_part} {mood_movies_part})"

    def __str__(self):
        """
        String representation of the user and their favorite and mood-based movies.
        """
        favorite_movie_list = "\n".join([f"- {movie.title}" for movie in self.favorite_movies])
        mood_movie_list = "\n".join([f"- {movie.title}" for movie in self.mood_movies])

        return (
            f"User: {self.name}, Age: {self.age}\n"
            f"Favorite Movies:\n{favorite_movie_list}\n"
            f"Movies by Mood:\n{mood_movie_list}"
        )
