from movies_api.models import Movie
from movies_api.repository import AbstractRepository


class MovieService:
    repository: AbstractRepository[Movie]

    def __init__(self, repository: AbstractRepository[Movie]) -> None:
        self.repository = repository

    def add_movies(self, *movies: Movie) -> list[Movie]:
        result: list[Movie] = self.repository.insert(*movies)
        return result
