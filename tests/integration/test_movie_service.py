"""Tests for adding movies"""

from decimal import Decimal
from assertpy import assert_that
import pytest

from movies_api.models import Movie
from movies_api.service import AggregateException, MovieService
from movies_api.repository import FakeMovieRepository


@pytest.fixture()
def service(repository: FakeMovieRepository) -> MovieService:
    return MovieService(repository)


class TestAddMoviesUseCase:
    def test_should_add_one_movie(self, service: MovieService) -> None:
        movie = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))

        service.add_movies(movie)
        first, *_ = service.list()

        assert_that(first).has_name("The Matrix").has_year(1999).has_rating(8.7)

    def test_should_add_multiple_movies(self, service: MovieService) -> None:
        movie1 = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))
        movie2 = Movie(name="The Matrix Reloaded", year=2003, rating=Decimal(7.7))

        service.add_movies(movie1, movie2)
        first, second = service.list()

        assert_that(first).has_name("The Matrix").has_year(1999).has_rating(8.7)
        assert_that(second).has_name("The Matrix Reloaded").has_year(2003).has_rating(7.7)


class TestRemoveMoviesUseCase:
    def test_should_fail_removing_non_existing_movie(self, service: MovieService) -> None:
        movie = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))

        assert_that(service.remove_movies).raises(AggregateException).when_called_with(movie)

    def test_should_remove_one_movie(self, service: MovieService) -> None:
        movie = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))
        service.add_movies(movie)

        service.remove_movies(movie)
        movies = service.list()

        assert_that(movies).is_empty()

    def test_should_remove_multiple_movies(self, service: MovieService) -> None:
        movie1 = Movie(name="The Matrix", year=1999, rating=Decimal(8.7))
        movie2 = Movie(name="The Matrix Reloaded", year=2003, rating=Decimal(7.7))
        service.add_movies(movie1, movie2)

        service.remove_movies(movie1)
        movies = service.list()

        assert_that(movies).is_length(1)
