from flask import Blueprint, render_template, redirect, request, url_for
from flask_jwt_extended import jwt_required

from cinema.models.movies import MovieModel
from ..decorators import admin_group_required

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/all/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_movies():
    """Return page with all movies"""

    movies = MovieModel.return_all(to_dict=False)
    return render_template("cinema/movies/movie_list.html", movies=movies)


@movies_bp.route("/", methods=["GET"])
def get_movies_in_rental():
    """Return page with all movies whiche in rental"""

    movies = MovieModel.return_all_in_rental(to_dict=False)
    return render_template("cinema/movies/movie_list.html", movies=movies)


@movies_bp.route("/<int:movie_id>/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_movie(movie_id):
    """Return page with movie by id"""

    movie = MovieModel.find_by_id(movie_id)
    if not movie:
        return render_template(
            "cinema/movies/movie_error.html", message="Movie not found"
        )

    return render_template("cinema/movies/movie_detail.html", movie=movie)


@movies_bp.route("/create/", methods=["GET", "POST"])
@jwt_required()
@admin_group_required
def add_movie():
    """Render page for create movie if method - GET
    and post form with movie data if method - POST
    """

    if request.method == "GET":
        return render_template("cinema/movies/movie_add.html")
    if not request.form:
        return render_template(
            "cinema/movies/movie_error.html", message="Something was wrong."
        )

    title = request.form.get("title")
    duration = int(request.form.get("duration"))
    description = request.form.get("description")
    year = int(request.form.get("year"))
    genres = request.form.get("genres")
    actors = request.form.get("actors")
    producer = request.form.get("producer")
    age_rating = request.form.get("age_rating")

    movie = MovieModel(
        title=title,
        duration=duration,
        description=description,
        year=year,
        genres=genres,
        actors=actors,
        producer=producer,
        age_rating=age_rating,
    )
    movie.save_to_db()

    return redirect(url_for("movies.get_movie", movie_id=movie.id))


@movies_bp.route("/update/<int:movie_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def update_movie(movie_id):
    """Render page for update movie by id if method - GET
    and post form with movie data if method - POST
    """

    movie = MovieModel.find_by_id(movie_id)

    if not movie:
        return render_template(
            "cinema/movies/movie_error.html", message="Movie not found"
        )
    if request.method == "GET":
        return render_template("cinema/movies/movie_update.html", movie=movie)

    title = request.form.get("title")
    duration = request.form.get("duration")
    description = request.form.get("description")
    year = request.form.get("year")
    genres = request.form.get("genres")
    actors = request.form.get("actors")
    producer = request.form.get("producer")
    age_rate = request.form.get("age_rate")

    if title:
        movie.title = title
    if duration:
        movie.duration = duration
    if description:
        movie.description = description
    if year:
        movie.year = year
    if genres:
        movie.genres = genres
    if age_rate:
        movie.age_rate = age_rate
    if actors:
        movie.actors = actors
    if producer:
        movie.producer = producer

    movie.save_to_db()

    return redirect(url_for("movies.get_movie", movie_id=movie.id))


@movies_bp.route("/delete/<int:movie_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def delete_movie(movie_id):
    """Render page for delete movie if method - GET
    and delete movie by id if method - POST
    """

    if request.method == "GET":
        movie = MovieModel.find_by_id(movie_id, to_dict=False)
        return render_template("cinema/movies/movie_delete.html", movie=movie)
    if request.method == "POST":
        code = MovieModel.delete_by_id(movie_id)
        if code == 404:
            return render_template(
                "cinema/movies/movie_error.html", message="Session not found"
            )

    return redirect(url_for("movies.get_movies"))
