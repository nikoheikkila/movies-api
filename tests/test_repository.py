from assertpy import assert_that

from movies_api.service import Movie
from movies_api.repository import FakeMovieRepository


class TestFakeRepository:
    def test_insert_one(self, repository: FakeMovieRepository) -> None:
        movie = Movie(name="Repo Man", year=1984, rating=6.9)

        repository.insert(movie)

        assert_that(repository.items).is_length(1).contains(movie)

    def test_insert_many(self, repository: FakeMovieRepository) -> None:
        first = Movie(name="Repo Man", year=1984, rating=6.9)
        second = Movie(name="Repo Men", year=2010, rating=6.3)

        repository.insert(first, second)

        assert_that(repository.items).is_length(2).contains(first).contains(second)
