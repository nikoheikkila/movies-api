from movies_api.models import Movie
from movies_api.repository import AbstractRepository


class AggregateException(Exception):
    pass


class MovieService:
    repository: AbstractRepository[Movie]

    def __init__(self, repository: AbstractRepository[Movie]) -> None:
        self.repository = repository

    def add_movies(self, *movies: Movie) -> list[Movie]:
        return self.repository.insert(*movies)

    def remove_movies(self, *movies: Movie) -> None:
        try:
            self.repository.delete(*movies)
        except ValueError as e:
            raise AggregateException(e)

    def list(self) -> list[Movie]:
        return self.repository.items
