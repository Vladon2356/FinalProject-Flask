from flask import request, Blueprint, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    get_jwt_identity,
)

from cinema.models.revoked_token import RevokedTokenModel
from cinema.models.users import UserModel

auth_bp = Blueprint("auth", __name__)


def add_groups(new_user):
    """Add lable admin if user is admin"""
    in_groups = []
    if new_user.is_admin:
        in_groups.append("admin")
    return in_groups


@auth_bp.route("/registration/", methods=["POST", "GET"])
def register():
    """Method for adding a new user (registration).
    Returns access and refresh tokens.
    """
    if request.method == "GET":
        return render_template("cinema/auth/user_regestri.html")
    if not request.form:
        return render_template(
            "cinema/users/user_error.html", message="Something was wrong"
        )

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    age = int(request.form["age"])
    email = request.form["email"]
    password = request.form["password"]

    if UserModel.find_by_first_and_last_name(
        first_name=first_name, last_name=last_name
    ):
        return render_template(
            "cinema/users/user_error.html",
            message=f"User with username - {first_name + ' ' + last_name} already exist",
        )

    if UserModel.find_by_email(email):
        return render_template(
            "cinema/users/user_error.html",
            message=f"User with email - {email} already exists",
        )

    new_user = UserModel(
        first_name=first_name,
        last_name=last_name,
        age=age,
        email=email,
        hashed_password=UserModel.generate_hash(password),
    )
    try:
        new_user.save_to_db()
        username = first_name + " " + last_name
        groups = {"groups": add_groups(new_user)}
        access_token = create_access_token(identity=username, additional_claims=groups)
        refresh_token = create_refresh_token(
            identity=username, additional_claims=groups
        )
        return {
            "message": f"User {username} was created",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except Exception as e:
        raise
        return {"message": "Something went wrong while creating", "error": repr(e)}, 500


@auth_bp.route("/login/", methods=["POST", "GET"])
def login():
    """Method for logination. Returns access and refresh tokens."""
    if request.method == "GET":
        return render_template("cinema/auth/user_login.html")
    if not request.form:
        return render_template(
            "cinema/users/user_error.html", message="Something went wrong while login"
        )
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    username = first_name + " " + last_name
    password = request.form["password"]
    current_user = UserModel.find_by_first_and_last_name(
        first_name=first_name, last_name=last_name, to_dict=False
    )
    if not current_user:
        return {"message": f"User {username} doesn't exist"}

    groups = {"groups": add_groups(current_user)}
    if UserModel.verify_hash(password, current_user.hashed_password):
        access_token = create_access_token(identity=username, additional_claims=groups)
        refresh_token = create_refresh_token(
            identity=username, additional_claims=groups
        )
        return {
            "message": f"Logged in as { username }",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    else:
        return {"message": "Wrong password"}, 401


@auth_bp.route("/refresh/", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Method for refreshing access token. Returns new access token."""
    current_user_identity = get_jwt_identity()
    user = UserModel.find_by_first_and_last_name(current_user_identity, to_dict=False)

    groups = {"groups": add_groups(user)}
    access_token = create_access_token(
        identity=current_user_identity, additional_claims=groups
    )
    return {"access_token": access_token}


@auth_bp.route("/logout-access/", methods=["POST"])
@jwt_required()
def logout_access():
    """Method for logout from account. Required accsess token"""
    jti = get_jwt()["jti"]
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": "Access token has been revoked"}
    except Exception as e:
        return {
            "message": "Something went wrong while revoking token",
            "error": repr(e),
        }, 500


@auth_bp.route("/logout-refresh/", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    """Method for logout from account. Required refresh token"""

    jti = get_jwt()["jti"]
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": "Refresh token has been revoked"}
    except Exception:
        return {"message": "Something went wrong while revoking token"}, 500
