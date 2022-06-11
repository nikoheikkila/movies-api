from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    name: str
    year: int
    rating: float


class MovieService:
    def add_movies(self, *movies: Movie) -> list[Movie]:
        return list(movies)
