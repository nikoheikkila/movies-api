from typing import Generic, TypeVar

from movies_api.service import Movie

T = TypeVar("T")


class AbstractRepository(Generic[T]):
    def insert(self, *items: T) -> None:
        raise NotImplementedError  # pragma: no cover

    def items(self) -> list[T]:
        raise NotImplementedError  # pragma: no cover


class FakeMovieRepository(AbstractRepository[Movie]):
    __items: list[Movie]

    def __init__(self) -> None:
        self.__items = []

    @property
    def items(self) -> list[Movie]:
        return self.__items

    def insert(self, *items: Movie) -> None:
        self.__items.extend(items)
