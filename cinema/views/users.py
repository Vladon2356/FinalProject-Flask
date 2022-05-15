from flask import Blueprint, render_template, redirect, request, url_for
from flask_jwt_extended import jwt_required

from cinema.models.tickets import TicketModel
from cinema.models.users import UserModel
from ..decorators import admin_group_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/all/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_all_users():
    """Return page with all users"""
    users = UserModel.return_all()
    return render_template("cinema/users/users_list.html", users=users)


@users_bp.route("/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_all_active_users():
    """Return page with all users"""
    users = UserModel.return_all_is_active()
    return render_template("cinema/users/users_list.html", users=users)


@users_bp.route("/<int:user_id>/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_user(user_id):
    """Return page with user by id"""
    user = UserModel.find_by_id(user_id)
    tickets = TicketModel.find_by_owner_id(owner_id=user_id)
    if not user:
        return render_template("cinema/users/user_error.html", message="User not found")

    return render_template("cinema/users/user_detail.html", user=user, tickets=tickets)


@users_bp.route("/create/", methods=["POST", "GET"])
def create_user():
    """Render page for create user if method - GET
    and post form with user data if method - POST
    """
    if request.method == "GET":
        return render_template("cinema/users/user_create.html")
    if not request.form:
        return render_template(
            "cinema/users/user_error.html", message="Something was wrong."
        )

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")
    email = request.form.get("email")
    password = request.form.get("password")
    is_admin = request.form.get("is_admin") != None

    user = UserModel(
        first_name=first_name,
        last_name=last_name,
        age=age,
        email=email,
        is_admin=is_admin,
        hashed_password=UserModel.generate_hash(password),
    )
    user.save_to_db()

    return redirect(url_for("users.get_user", user_id=user.id))


@users_bp.route("/update/<int:user_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def update_user(user_id):
    """Render page for update user by id if method - GET
    and post form with user data if method - POST
    """
    user = UserModel.find_by_id(id=user_id)
    if not user:
        return render_template("cinema/users/user_error.html", message="User not found")
    if request.method == "GET":
        return render_template("cinema/users/user_update.html", user=user)
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")
    email = request.form.get("email")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    is_admin = request.form.get("is_admin") != None
    if UserModel.verify_hash(old_password, user.hashed_password):
        user.hashed_password = UserModel.generate_hash(new_password)
    if age:
        user.age = age
    if first_name and last_name:
        if not UserModel.find_by_first_and_last_name(
                first_name=first_name, last_name=last_name
        ):
            user.first_name = first_name
            user.last_name = last_name
    if email:
        user.email = email
    if is_admin:
        user.is_admin = is_admin
    user.save_to_db()
    return redirect(url_for("users.get_user", user_id=user.id))


@users_bp.route("/delete/<int:user_id>/", methods=["POST", "GET"])
@jwt_required()
@admin_group_required
def delete_user(user_id):
    """Render page for delete user if method - GET
    and delete user by id if method - POST
    """
    user = UserModel.find_by_id(id=user_id)
    if request.method == "GET":
        return render_template("cinema/users/user_delete.html", user=user)
    if request.method == "POST":
        code = UserModel.delete_by_id(user_id)
        if code == 404:
            return render_template(
                "cinema/users/user_error.html", message="User not found"
            )

    return redirect(url_for("users.get_users"))
