from contextlib import contextmanager
from typing import Generator, Generic, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from movies_api.models import Base, Movie

T = TypeVar("T", bound=Base)


class AbstractRepository(Generic[T]):
    @property
    def items(self) -> list[T]:
        raise NotImplementedError  # pragma: no cover

    def insert(self, *items: T) -> list[T]:
        raise NotImplementedError  # pragma: no cover

    def delete(self, *items: T) -> None:
        raise NotImplementedError  # pragma: no cover


class FakeMovieRepository(AbstractRepository[Movie]):
    __items: list[Movie]

    def __init__(self) -> None:
        self.__items = []

    @property
    def items(self) -> list[Movie]:
        return self.__items

    def insert(self, *items: Movie) -> list[Movie]:
        self.__items.extend(items)
        return list(items)

    def delete(self, *items: Movie) -> None:
        for item in items:
            self.__items.remove(item)


class MovieRepository(AbstractRepository[Movie]):
    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        Base.metadata.create_all(self.engine)

    @classmethod
    def with_memory(cls) -> "MovieRepository":
        return cls(engine=create_engine("sqlite:///:memory:"))

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        yield Session(self.engine)

    @property
    def items(self) -> list[Movie]:
        with self.session() as session:
            rows: list[Movie] = session.query(Movie).all()

        return rows

    def insert(self, *items: Movie) -> list[Movie]:
        with self.session() as session:
            session.add_all(items)
            session.commit()

        return list(items)

    def delete(self, *items: Movie) -> None:
        with self.session() as session:
            for item in items:
                session.delete(item)  # type: ignore

            session.commit()
