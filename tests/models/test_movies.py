from cinema import models


def test_find_by_id(create_movie):
    movie1 = create_movie
    movie = models.MovieModel.find_by_id(movie1.id)
    assert movie.id == movie1.id
    assert movie == movie1


def test_find_by_wrong_id(create_movie):
    movie1 = create_movie
    movie = models.MovieModel.find_by_id(999)
    assert movie == {}


def test_find_by_title(create_movie):
    movie1 = create_movie
    movie = models.MovieModel.find_by_title(movie1.title)
    assert movie.title == movie1.title


def test_find_by_not_extist_title(create_movie):
    movie1 = create_movie
    movie = models.MovieModel.find_by_title("XXXXXXX")
    assert movie == {}


def test_movies_return_all(create_movie):
    movie = create_movie
    movies = models.MovieModel.return_all()
    assert movie in movies


def test_movies_return_all_in_rental(create_movie, movie_factory):
    movie_in_rental = create_movie
    movie_not_in_rental = movie_factory(
        title="TestTitle",
        description="Something",
        year=2022,
        duration=123,
        genres="Fantasy, Marvel",
        actors="Tom Hardy",
        producer="Kevin Faigy",
        age_rating="G",
        in_rental=False,
    )
    movies = models.MovieModel.return_all_in_rental()
    assert movie_in_rental in movies
    assert movie_not_in_rental not in movies


def test_delete_by_id(create_movie):
    movie1 = create_movie
    code = models.MovieModel.delete_by_id(movie1.id)
    assert code == 200


def test_delete_by_not_exist_id():
    code = models.MovieModel.delete_by_id(999)
    assert code == 404


def test_to_dict_for_movie_not_in_rental(movie_factory):
    movie_not_in_rental = movie_factory(
        title="TestTitle",
        description="Something",
        year=2022,
        duration=123,
        genres="Fantasy, Marvel",
        actors="Tom Hardy",
        producer="Kevin Faigy",
        age_rating="G",
        in_rental=False,
    )
    res = models.MovieModel.to_dict(movie_not_in_rental)
    assert res["message"] == "Movie not in rental"


def test_to_dict_for_movie_in_rental(movie_factory):
    movie_in_rental = movie_factory(
        title="TestTitle",
        description="Something",
        year=2022,
        duration=123,
        genres="Fantasy, Marvel",
        actors="Tom Hardy",
        producer="Kevin Faigy",
        age_rating="G",
        in_rental=True,
    )

    res = models.MovieModel.to_dict(movie_in_rental)
    assert res["id"] == movie_in_rental.id
    assert res["title"] == movie_in_rental.title
    assert res["description"] == movie_in_rental.description
    assert res["duration"] == movie_in_rental.duration
    assert res["year"] == movie_in_rental.year
    assert res["actors"] == movie_in_rental.actors
    assert res["producer"] == movie_in_rental.producer
    assert res["genres"] == movie_in_rental.genres
    assert res["age_rating"] == movie_in_rental.age_rating
