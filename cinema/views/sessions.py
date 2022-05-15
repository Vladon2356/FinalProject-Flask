import datetime

from flask import Blueprint, render_template, redirect, request, url_for
from flask_jwt_extended import jwt_required

from cinema.models.halls import HallModel
from cinema.models.movies import MovieModel
from cinema.models.session import SessionModel
from cinema.models.tickets import TicketModel
from ..decorators import admin_group_required

sessions_bp = Blueprint("sessions", __name__)


@sessions_bp.route("/", methods=["GET"])
def get_sessions():
    """Return page with all sessions"""

    sessions = SessionModel.return_all(to_dict=False)

    return render_template("cinema/sessions/session_list.html", sessions=sessions)


@sessions_bp.route("/<int:session_id>", methods=["GET"])
def get_session_by_id(session_id):
    """Return page with session by id"""

    session = SessionModel.find_by_id(id=session_id, to_dict=False)
    if not session:
        return render_template(
            "cinema/sessions/session_error.html", message="Session not found"
        )
    tickets = TicketModel.find_by_session_id(session_id=session_id, to_dict=False)
    return render_template(
        "cinema/sessions/session_detail.html", session=session, tickets=tickets
    )


@sessions_bp.route("movie/<int:movie_id>", methods=["GET"])
def get_sessions_by_movie_id(movie_id):
    """Return page with session by id"""

    sessions = SessionModel.find_by_movie_id(movie_id=movie_id, to_dict=False)
    return render_template("cinema/sessions/session_list.html", session=sessions)




@sessions_bp.route("/search/", methods=["GET", "POST"])
def search_sessions():
    """Render page for serching"""
    movies = MovieModel.return_all_in_rental()
    if request.method == "GET":
        return render_template("cinema/sessions/session_search.html", movies=movies)

    movie_id = int(request.form.get("movie_id", 0))
    date_str = request.form.get("date", "")
    if date_str:
        month, day, year = [int(i) for i in date_str.split("/")]
        date = datetime.date(day=day, month=month, year=year)
    else:
        date = datetime.date(day=1, month=1, year=2000)
    genres = request.form.get("genres", "")
    actors = request.form.get("actors", "")
    producer = request.form.get("producer", "")

    sessions = SessionModel.for_search(
        movie_id=movie_id, date=date, genres=genres, actors=actors, producer=producer
    )

    return render_template("cinema/sessions/session_list.html", sessions=sessions)


@sessions_bp.route("/create/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def create_session():
    """Render page for create session if method - GET
    and post form with session data if method - POST
    """

    if request.method == "GET":
        movies = MovieModel.return_all_in_rental(to_dict=False)
        halls = HallModel.return_all(to_dict=False)
        return render_template(
            "cinema/sessions/session_create.html", movies=movies, halls=halls
        )
    if not request.form:
        return render_template(
            "cinema/users/user_error.html", message="Something was wrong."
        )

    movie_id = int(request.form.get("movie_id"))
    hall_id = int(request.form.get("hall_id"))
    date_str = request.form.get("date")
    start_at = request.form.get("start_at")
    end_at = request.form.get("end_at")
    tickets_price = int(request.form.get("tickets_price"))
    month, day, year = [int(i) for i in date_str.split("/")]
    date = datetime.date(day=day, month=month, year=year)
    session = SessionModel(
        movie_id=movie_id,
        hall_id=hall_id,
        date=date,
        start_at=start_at,
        end_at=end_at,
        tickets_price=tickets_price,
    )
    session.save_to_db()
    TicketModel.generage_tickets_for_session(session_id=session.id)
    return redirect(url_for("tickets.get_sessions_by_movie_id", session_id=session.id))


@sessions_bp.route("/update/<int:session_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def update_session(session_id):
    """Render page for update session by id if method - GET
    and post form with session data if method - POST
    """
    if request.method == "GET":
        movies = MovieModel.return_all_in_rental(to_dict=False)
        halls = HallModel.return_all(to_dict=False)
        session = SessionModel.find_by_id(id=session_id)
        return render_template(
            "cinema/sessions/session_update.html",
            session=session,
            movies=movies,
            halls=halls,
        )
    movie_id = int(request.form.get("movie_id"))
    hall_id = int(request.form.get("hall_id"))
    start_at = request.form.get("start_at")
    end_at = request.form.get("end_at")

    session = SessionModel.find_by_id(session_id, to_dict=False)
    if not session:
        return render_template(
            "cinema/sessions/session_error.html", message="User not found"
        )
    if movie_id:
        session.movie_id = movie_id
    if hall_id:
        session.hall_id = hall_id
    if start_at:
        session.start_at = start_at
    if end_at:
        session.end_at = end_at
    session.save_to_db()
    return redirect(url_for("sessions.get_session_by_id", session_id=session.id))


@sessions_bp.route("/delete/<int:session_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def delete_session(session_id):
    """Render page for delete session if method - GET
    and delete session by id if method - POST
    """
    if request.method == "GET":
        return render_template("cinema/sessions/session_delete.html")
    if request.method == "POST":
        code = SessionModel.delete_by_id(session_id)
        if code == 404:
            return render_template(
                "cinema/sessions/session_error.html", message="Session not found"
            )

    return redirect(url_for("sessions.get_sessions"))
