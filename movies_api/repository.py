from typing import Generic, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from movies_api.models import Movie, Base

T = TypeVar("T", bound=Base)


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


class MovieRepository(AbstractRepository[Movie]):
    session: sessionmaker

    def __init__(self, engine: Engine) -> None:
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)

    @classmethod
    def with_memory(cls) -> "MovieRepository":
        return cls(engine=create_engine("sqlite:///:memory:"))

    def insert(self, *items: Movie) -> None:
        with self.session() as session:
            session.add_all(items)
            session.commit()

    @property
    def items(self) -> list[Movie]:
        with self.session() as session:
            rows: list[Movie] = session.query(Movie).all()

        return rows
