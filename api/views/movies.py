from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from cinema.models.movies import MovieModel
from cinema.decorators import admin_group_required

movies_api_bp = Blueprint("movies_api", __name__)


@movies_api_bp.route("/", methods=["GET"])
def get_movies():
    movies = MovieModel.return_all_in_rental(to_dict=True)
    return jsonify(movies)


@movies_api_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = MovieModel.find_by_id(id=movie_id, to_dict=True)
    if not movie:
        return jsonify({"message": "Movie not found."}), 404
    return jsonify(movie)
