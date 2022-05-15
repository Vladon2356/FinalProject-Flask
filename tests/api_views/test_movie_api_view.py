from flask import url_for


def test_get_movies(client, create_movie, movie_factory):
    movie1 = create_movie
    movie2 = movie_factory(
        title="Test Title 2",
        description="XXXXX",
        year=2022,
        duration=140,
        genres="Marvel",
        actors="Tom Hardy",
        producer="Kevin Faigy",
        age_rating="G",
        in_rental=True,
    )
    movie2.save_to_db()
    response = client.get(url_for("movies_api.get_movies"))
    assert response.status_code == 200
    for movie in response.json:
        assert movie["actors"]
        assert movie["age_rating"]
        assert movie["description"]
        assert movie["duration"]
        assert movie["genres"]
        assert movie["id"]
        assert movie["producer"]
        assert movie["title"]
        assert movie["year"]


def test_get_movie(client, create_movie):
    movie = create_movie
    response = client.get(url_for("movies_api.get_movie", movie_id=movie.id))
    res = response.json
    assert response.status_code == 200
    assert res["id"] == movie.id
    assert res["title"] == movie.title
    assert res["actors"] == movie.actors
    assert res["age_rating"] == movie.age_rating
    assert res["description"] == movie.description
    assert res["duration"] == movie.duration
    assert res["genres"] == movie.genres
    assert res["producer"] == movie.producer
    assert res["year"] == movie.year


def test_get_movie_by_not_exist_id(client):
    response = client.get(url_for("movies_api.get_movie", movie_id=9999))

    assert response.status_code == 404
    assert response.json["message"] == "Movie not found."
