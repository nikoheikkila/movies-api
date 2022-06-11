"""Tests for adding movies"""

from assertpy import assert_that

from movies_api.service import MovieService, Movie


class TestAddMovies:
    def test_can_add_one_movie(self) -> None:
        service = MovieService()
        movie = Movie(name="The Matrix", year=1999, rating=8.7)

        first, *_ = service.add_movies(movie)

        assert_that(first).has_name("The Matrix").has_year(1999).has_rating(8.7)

    def test_can_add_multiple_movies(self) -> None:
        service = MovieService()
        movie1 = Movie(name="The Matrix", year=1999, rating=8.7)
        movie2 = Movie(name="The Matrix Reloaded", year=2003, rating=7.7)

        first, second = service.add_movies(movie1, movie2)

        assert_that(first).has_name("The Matrix").has_year(1999).has_rating(8.7)
        assert_that(second).has_name("The Matrix Reloaded").has_year(2003).has_rating(7.7)
