# Movies API

A simple Python backend project storing data about the movies I've watched.

The purpose is to practice and learn domain-driven design, hexagonal architecture, and test-driven development among other things fostering the technical excellence practices.

## Use Cases

The main aggregate (_Movie_) has following use cases:

- adding one or more movies
- removing one or more movies
- listing all movies

The behaviour of aggregate and its related service can be found in [integration tests](./tests/integration/test_movie_service.py).

## Repository

Project is backed with repository pattern that connects to an SQLite database (either in-memory or in-file). Tests integrate with fake repository, which emulates the database using a standard Python list type.

## Commands

The following commands require `task` runner installed, see [here](https://taskfile.dev).

- `task format` to format codebase
- `task lint` to lint codebase for style issues
- `task test` to run all tests with coverage measurements
