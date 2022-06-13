from decimal import Decimal
from assertpy import assert_that

from movies_api.models import Movie
from movies_api.repository import MovieRepository


class TestMovieRepository:
    def test_insert_one(self) -> None:
        repository = MovieRepository.with_memory()
        movie = Movie(name="Repo Man", year=1984, rating=Decimal(6.9))

        repository.insert(movie)
        first, *_ = repository.items

        assert_that(first).is_instance_of(Movie).has_name("Repo Man").has_year(1984).has_rating(6.9)

    def test_insert_many(self) -> None:
        repository = MovieRepository.with_memory()
        movie1 = Movie(name="Repo Man", year=1984, rating=Decimal(6.9))
        movie2 = Movie(name="Repo Men", year=2010, rating=Decimal(6.3))

        repository.insert(movie1, movie2)
        first, second = repository.items

        assert_that(first).is_instance_of(Movie).has_name("Repo Man").has_year(1984).has_rating(6.9)
        assert_that(second).is_instance_of(Movie).has_name("Repo Men").has_year(2010).has_rating(6.3)

    def test_remove_one(self) -> None:
        repository = MovieRepository.with_memory()
        movie = Movie(name="Repo Man", year=1984, rating=Decimal(6.9))
        repository.insert(movie)

        repository.delete(movie)
        items = repository.items

        assert_that(items).is_empty()

    def test_remove_many(self) -> None:
        repository = MovieRepository.with_memory()
        movie1 = Movie(name="Repo Man", year=1984, rating=Decimal(6.9))
        movie2 = Movie(name="Repo Men", year=2010, rating=Decimal(6.3))
        repository.insert(movie1, movie2)

        repository.delete(movie1, movie2)
        items = repository.items

        assert_that(items).is_empty()
