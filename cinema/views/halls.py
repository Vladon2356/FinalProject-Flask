from flask import Blueprint, render_template, redirect, request, url_for
from flask_jwt_extended import jwt_required

from cinema.models.halls import HallModel
from ..decorators import admin_group_required

halls_bp = Blueprint("halls", __name__)


@halls_bp.route("/", methods=["GET"])
def get_halls():
    """Return page with all halls"""

    halls = HallModel.return_all()

    return render_template("cinema/halls/hall_list.html", halls=halls)


@halls_bp.route("/<int:hall_id>", methods=["GET"])
def get_hall(hall_id):
    """Return page of hall with id=id_"""
    hall = HallModel.find_by_id(id=hall_id)

    return render_template("cinema/halls/hall_detail.html", hall=hall)


@halls_bp.route("/create/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def create_hall():
    """Render page for create hall if method - GET
    and post form with hall data if method - POST
    """

    if request.method == "GET":
        return render_template("cinema/halls/hall_create.html")
    if not request.form:
        return render_template(
            "cinema/users/user_error.html", message="Something was wrong."
        )

    title = request.form.get("title")
    rows = int(request.form.get("rows"))
    columns = int(request.form.get("columns"))

    hall = HallModel(title=title, rows=rows, columns=columns)
    hall.save_to_db()

    return redirect(url_for("halls.get_halls", hall_id=hall.id))


@halls_bp.route("/update/<int:hall_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def update_hall(hall_id):
    """Render page for update hall if method - GET
    and post form with hall data if method - POST
    """

    if request.method == "GET":
        hall = HallModel.find_by_id(id=hall_id)
        return render_template("cinema/halls/hall_update.html", hall=hall)
    title = request.form.get("title")
    rows = request.form.get("rows")
    columns = request.form.get("columns")
    hall = HallModel.find_by_id(hall_id)
    if not hall:
        return render_template("cinema/halls/hall_error.html", message="Hall not found")
    if title:
        hall.title = title
    if rows:
        hall.rows = rows
    if columns:
        hall.columns = columns
    hall.save_to_db()
    return redirect(url_for("halls.get_hall", hall_id=hall.id))


@halls_bp.route("/delete/<int:hall_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def delete_hall(hall_id):
    """Render page for delete hall if method - GET
    and delete hall by id if method - POST
    """
    if request.method == "GET":
        return render_template("cinema/halls/hall_delete.html")
    if request.method == "POST":
        code = HallModel.delete_by_id(hall_id)
        if code == 404:
            return render_template(
                "cinema/halls/hall_error.html", message="hall not found"
            )

    return redirect(url_for("get_halls"))
