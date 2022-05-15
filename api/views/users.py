from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from cinema.models.users import UserModel
from cinema.decorators import admin_group_required

users_api_bp = Blueprint("users_api", __name__)


@users_api_bp.route("/", methods=["GET"])
@jwt_required()
@admin_group_required
def get_users():
    users = UserModel.return_all_is_active(to_dict=True)
    return jsonify(users)


@users_api_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@admin_group_required
def get_user(user_id):
    user = UserModel.find_by_id(id=user_id, to_dict=True)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user)


@users_api_bp.route("/me/", methods=["GET"])
@jwt_required()
def get_me():
    current_user_identity = get_jwt_identity()
    first_name, last_name = current_user_identity.split(" ")
    user = UserModel.find_by_first_and_last_name(
        first_name=first_name, last_name=last_name, to_dict=True
    )
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user)
