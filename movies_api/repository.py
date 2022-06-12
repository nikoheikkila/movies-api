from contextlib import contextmanager
from typing import Generator, Generic, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from movies_api.models import Base, Movie

T = TypeVar("T", bound=Base)


class AbstractRepository(Generic[T]):
    def insert(self, *items: T) -> list[T]:
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

    def insert(self, *items: Movie) -> list[Movie]:
        self.__items.extend(items)
        return list(items)


class MovieRepository(AbstractRepository[Movie]):
    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        yield Session(self.engine)

    @classmethod
    def with_memory(cls) -> "MovieRepository":
        return cls(engine=create_engine("sqlite:///:memory:"))

    def insert(self, *items: Movie) -> list[Movie]:
        with self.session() as session:
            session.add_all(items)
            session.commit()

        return list(items)

    @property
    def items(self) -> list[Movie]:
        with self.session() as session:
            rows: list[Movie] = session.query(Movie).all()

        return rows
