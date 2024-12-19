from typing import List, Dict

TMDB_URL = "https://api.themoviedb.org/3/movie/"
CACHE_FILE = "movies_cache.json"


class Movie:
    """
    A class to represent a movie with attributes like title, genre_ids, release_date, popularity, etc.

    Attributes:
        id (int): the id of the movie.
        title (str): The title of the movie.
        genre_ids (List[int]): List of genre IDs associated with the movie.
        release_date (str): Release date of the movie in 'YYYY-MM-DD' format.
        popularity (float): Popularity score of the movie.
        vote_average (float): Average rating of the movie based on user votes.
        adult (bool): Indicates if the movie is restricted to adult audiences.
        original_language (str): The original language of the movie.
        poster_path (str): The original poster of the movie
    """

    def __init__(
            self,
            id: int,
            title: str,
            genre_ids: List[int],
            release_date: str,
            popularity: float,
            vote_average: float,
            adult: bool,
            original_language: str,
            poster_path: str = "",
    ):
        """
        Initializes a Movie instance.

        :param id: The id of the movie.
        :param title: The title of the movie.
        :param genre_ids: List of genre IDs associated with the movie.
        :param release_date: Release date of the movie in 'YYYY-MM-DD' format.
        :param popularity: Popularity score of the movie.
        :param vote_average: Average rating of the movie based on user votes.
        :param adult: Indicates if the movie is restricted to adult audiences.
        :param original_language: The original language of the movie.
        :param poster_path: The original poster of the movie
        """
        self._id = id
        self._title = title
        self._genre_ids = genre_ids
        self._release_date = release_date
        self._popularity = popularity
        self._vote_average = vote_average
        self._adult = adult
        self._original_language = original_language
        self._poster_path = poster_path

    ####################################################################################################################
    # Properties and setters
    ####################################################################################################################
    @property
    def id(self) -> int:
        """
        Gets the id of the movie.
        :return: The id of the movie.
        """
        return self._id

    @id.setter
    def id(self, value: int):
        """
        Sets the id of the movie.
        :param value: The id of the movie.
        :raises TypeError: If the id is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError("Id must be an integer.")
        self._id = value

    @property
    def poster_path(self) -> str:
        """
        Represents the file path or URL to the poster image for a particular entity.
        This property provides access to the string value representing the path
        or URI that points to the poster image. It is typically utilized to
        display the visual representation of the entity in user interfaces.

        :return: The path or URL to the poster image.
        :rtype: str
        """
        return self._poster_path

    @poster_path.setter
    def poster_path(self, value: str):
        """
        Set the title of the media object.

        The title is an essential attribute for a media object and provides the name or
        designation for the media. This setter ensures the value assigned to the title is
        properly validated and set for further use.

        :param value: The new value to set as the title
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        self._title = value

    @property
    def title(self) -> str:
        """
        Gets the title of the movie.

        :return: The title of the movie.
        """
        return self._title

    @title.setter
    def title(self, value: str):
        """
        Sets the title of the movie.

        :param value: The title as a string.
        :raises TypeError: If the title is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        self._title = value

    @property
    def genre_ids(self) -> List[int]:
        """
        Gets the genre IDs of the movie.

        :return: A list of genre IDs (integers).
        """
        return self._genre_ids

    @genre_ids.setter
    def genre_ids(self, value: List[int]):
        """
        Sets the genre IDs of the movie.

        :param value: A list of integers representing genres.
        :raises TypeError: If genre IDs are not a list of integers.
        """
        if not all(isinstance(genre, int) for genre in value):
            raise TypeError("genre_ids must be a list of integers.")
        self._genre_ids = value

    @property
    def release_date(self) -> str:
        """
        Gets the release date of the movie.

        :return: The release date of the movie in 'YYYY-MM-DD' format.
        """
        return self._release_date

    @release_date.setter
    def release_date(self, value: str):
        """
        Sets the release date of the movie.

        :param value: A string in 'YYYY-MM-DD' format.
        """
        self._release_date = value

    @property
    def popularity(self) -> float:
        """
        Gets the popularity score of the movie.

        :return: The popularity score as a float.
        """
        return self._popularity

    @popularity.setter
    def popularity(self, value: float):
        """
        Sets the popularity score of the movie.

        :param value: A float value representing popularity.
        :raises TypeError: If the popularity is not a number.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Popularity must be a float or int.")
        self._popularity = float(value)

    @property
    def vote_average(self) -> float:
        """
        Gets the average vote rating of the movie.

        :return: The average rating as a float.
        """
        return self._vote_average

    @vote_average.setter
    def vote_average(self, value: float):
        """
        Sets the average vote rating of the movie.

        :param value: A float value for the rating.
        :raises TypeError: If the vote average is not a number.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Vote average must be a float or int.")
        self._vote_average = float(value)

    @property
    def adult(self) -> bool:
        """
        Gets the adult classification of the movie.

        :return: True if the movie is for adults, otherwise False.
        """
        return self._adult

    @adult.setter
    def adult(self, value: bool):
        """
        Sets the adult classification of the movie.

        :param value: A boolean indicating adult classification.
        :raises TypeError: If adult is not a boolean value.
        """
        if not isinstance(value, bool):
            raise TypeError("Adult must be a boolean.")
        self._adult = value

    @property
    def original_language(self) -> str:
        """
        Gets the original language of the movie.

        :return: The original language as a string.
        """
        return self._original_language

    @original_language.setter
    def original_language(self, value: str):
        """
        Sets the original language of the movie.

        :param value: A string representing the original language.
        :raises TypeError: If the original language is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Original language must be a string.")
        self._original_language = value

    ####################################################################################################################
    # Useful methods
    ####################################################################################################################
    @staticmethod
    def from_dict(data: Dict) -> "Movie":
        """
        Creates a Movie object from a dictionary.

        :param data: A dictionary containing movie data.
        :return: A Movie instance.
        """
        return Movie(
            id=data.get("id", 0),
            title=data.get("title", "Unknown"),
            genre_ids=data.get("genre_ids", []),
            release_date=data.get("release_date", "Unknown"),
            popularity=data.get("popularity", 0.0),
            vote_average=data.get("vote_average", 0.0),
            adult=data.get("adult", False),
            original_language=data.get("original_language", "Unknown"),
            poster_path=data.get("poster_path", ""),
        )

    def to_dict(self) -> Dict:
        """
        Converts the Movie object to a dictionary.

        :return: A dictionary representation of the movie.
        """
        return {
            "id": self._id,
            "title": self._title,
            "genre_ids": self._genre_ids,
            "release_date": self._release_date,
            "popularity": self._popularity,
            "vote_average": self._vote_average,
            "adult": self._adult,
            "original_language": self._original_language,
            "poster_path": self._poster_path,
        }

    def to_lisp(self) -> str:
        """
        Converts the Movie object into a Lisp cons pair structure.
        Example:
          ((:title . "Interstellar") (:genre_ids . (12 18 878)) ...)
        """

        def list_to_lisp(lst):
            return "(" + " ".join(str(x) for x in lst) + ")"

        parts = [f'(:title . "{self._title}")', f'(:id . {self._id})']
        if self._genre_ids:
            genre_list = list_to_lisp(self._genre_ids)
            parts.append(f'(:genre_ids . {genre_list})')
        else:
            parts.append('(:genre_ids . ())')
        parts.append(f'(:release_date . "{self._release_date}")')
        parts.append(f'(:popularity . {self._popularity})')
        parts.append(f'(:vote_average . {self._vote_average})')
        parts.append(f'(:adult . {"t" if self._adult else "nil"})')
        parts.append(f'(:original_language . "{self._original_language}")')
        if self._poster_path:
            parts.append(f'(:poster_path . "{self._poster_path}")')

        return "(" + " ".join(parts) + ")"

    def __str__(self) -> str:
        """
        Provides a string representation of the Movie object.

        :return: A formatted string with movie details.
        """
        return (
            f"ID: {self._id}\n"
            f"Title: {self._title}\n"
            f"Genres (IDs): {self._genre_ids}\n"
            f"Release Date: {self._release_date}\n"
            f"Popularity: {self._popularity}\n"
            f"Vote Average: {self._vote_average}\n"
            f"Adult: {'Yes' if self._adult else 'No'}\n"
            f"Original Language: {self._original_language}\n"
            f"Poster Path: {self._poster_path}"
        )
