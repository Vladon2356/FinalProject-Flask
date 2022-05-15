from flask import jsonify, request, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    get_jwt_identity,
)

from cinema.models.users import UserModel
from cinema.models.revoked_token import RevokedTokenModel

auth_api_bp = Blueprint("auth_api", __name__)


def add_groups(new_user):
    in_groups = []
    if new_user.is_admin:
        in_groups.append("admin")
    return in_groups


@auth_api_bp.route("/registration/", methods=["POST"])
def register():
    if not (
            request.json
            and request.json.get("first_name")
            and request.json.get("last_name")
            and request.json.get("password")
            and request.json.get("age")
            and request.json.get("email")

    ):
        return (
            jsonify(
                {
                    "message": 'Please, provide "age", "last_name", first_name", "email" and "password" in body.'
                }
            ),
            400,
        )
    """Method for adding a new user (registration).
    Returns access and refresh tokens.
    """

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    username = first_name + " " + last_name
    age = request.json["age"]
    email = request.json["email"]
    password = request.json["password"]
    is_admin = request.json.get("is_admin", False)

    if UserModel.find_by_first_and_last_name(
            first_name=first_name, last_name=last_name, to_dict=False
    ):
        return {"message": f"User with username - {username} already exists"}

    new_user = UserModel(
        first_name=first_name,
        last_name=last_name,
        age=age,
        is_admin=is_admin,
        email=email,
        hashed_password=UserModel.generate_hash(password),
    )
    try:
        new_user.save_to_db()

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


@auth_api_bp.route("/login/", methods=["POST"])
def login():
    """Method for logination. Returns access and refresh tokens."""
    if (
        not request.json
        or not request.json.get("first_name")
        or not request.json.get("last_name")
        or not request.json.get("password")
    ):
        return (
            jsonify(
                {
                    "message": 'Please, provide "first_name", "last_name" and "password" in body.'
                }
            ),
            400,
        )

    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    username = first_name + " " + last_name
    password = request.json["password"]
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
            "message": f"Logged in as {username}",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    else:
        return {"message": "Wrong password"}, 401


@auth_api_bp.route("/refresh/", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Method for refreshing access token. Returns new access token."""
    current_user_identity = get_jwt_identity()
    first_name, last_name = current_user_identity.split(" ")
    user = UserModel.find_by_first_and_last_name(
        first_name=first_name, last_name=last_name, to_dict=False
    )

    groups = {"groups": add_groups(user)}
    access_token = create_access_token(
        identity=current_user_identity, additional_claims=groups
    )
    return {"access_token": access_token}


@auth_api_bp.route("/logout-access", methods=["POST"])
@jwt_required()
def logout_access():
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


@auth_api_bp.route("/logout-refresh/", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]  # id of a jwt accessing this post method
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": "Refresh token has been revoked"}
    except Exception:
        return {"message": "Something went wrong while revoking token"}, 500
